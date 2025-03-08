import re
import json
import os
from google import genai
from django.conf import settings
from .models import ChatMessage
from lessons.views import api_lesson_detail



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class LLMClient:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client =genai.Client(api_key=GEMINI_API_KEY)
    def generate(self, prompt):
        try:
            response = self.client.models.generate_content(contents=prompt, 
                                                           model=self.model_name)
        except Exception as e:
            print("LLM generate fail: ", e)
        return response.text


class ConversationManager:
    MAX_HISTORY_LENGTH = 10
    SESSION_KEY = 'conversation'
    
    def __init__(self, session):
        self.session = session
        self._init_conversation()
        
    def _init_conversation(self):
        default_conversation = {
            'history': [],
            'summary': '',
            'lesson_stage': 'intro',
            'section_index': 0,
            'completed_topics': []
        }
        current = self.session.get(self.SESSION_KEY, {})
        # Merge existing data with defaults
        self.session[self.SESSION_KEY] = {**default_conversation, **current}
        self.session.modified = True
    
    # Add getters and setters for the new properties
    @property
    def lesson_stage(self):
        return self.session[self.SESSION_KEY]['lesson_stage']
    
    @lesson_stage.setter
    def lesson_stage(self, value):
        self.session[self.SESSION_KEY]['lesson_stage'] = value
        self.session.modified = True
    
    @property
    def section_index(self):
        try:
            return self.session[self.SESSION_KEY]['section_index']
        except KeyError:
            # Initialize missing key
            self.session[self.SESSION_KEY]['section_index'] = 0
            self.session.modified = True
            return 0
    
    @section_index.setter
    def section_index(self, value):
        self.session[self.SESSION_KEY]['section_index'] = value
        self.session.modified = True
        
    @property
    def completed_topics(self):
        return self.session[self.SESSION_KEY]['completed_topics']
    
    def add_completed_topic(self, topic_id):
        if topic_id not in self.completed_topics:
            self.completed_topics.append(topic_id)
            self.session.modified = True
    
    @property
    def history(self):
        return self.session[self.SESSION_KEY]['history']
    
    @property
    def summary(self):
        return self.session[self.SESSION_KEY]['summary']
    
    @summary.setter
    def summary(self, value):
        self.session[self.SESSION_KEY]['summary'] = value
        self.session.modified = True
    
    def add_message(self, role, content):
        self.history.append({role: content})
        if len(self.history) > self.MAX_HISTORY_LENGTH:
            self.history.pop(0)
        self.session.modified = True
    
    def get_formatted_history(self):
        return "\n".join(
            f"{'Học sinh' if 'user' in msg else 'Giảng viên'}: {list(msg.values())[0]}"
            for msg in self.history[-self.MAX_HISTORY_LENGTH:]
        )

class PromptEngine:
    PROMPT_TEMPLATE = '''
        **Vai trò:** Giảng viên Toán THPT Việt Nam, kiên nhẫn, tận tâm và ĐIỀU PHỐI quy trình học tập
        **Nhiệm vụ:** Trả lời câu hỏi của học sinh và điều hướng quá trình học theo các giai đoạn:
        
        **Thông tin bài học:**
        - Bài học hiện tại: {lesson_title}
        - Giai đoạn hiện tại: {lesson_stage}
        - Phần hiện tại: {section_index} của {total_sections}
        - Nội dung phần hiện tại: {current_section_title}
        
        **Quy trình hướng dẫn:**
        1. Giới thiệu bài học
        2. Trình bày kiến thức cơ bản
        3. Hướng dẫn ví dụ
        4. Giao bài tập thực hành
        5. Tổng kết bài học
        
        **Quy tắc điều phối:**
        - Khi học sinh đã hiểu phần hiện tại, chủ động đề xuất chuyển sang phần tiếp theo
        - Khi học sinh cần làm bài tập, đề xuất chuyển sang tab bài tập
        - Khi học sinh muốn xem ví dụ, đề xuất chuyển sang tab ví dụ
        - Khi hoàn thành bài học, đề xuất kết thúc và chuyển sang bài tiếp theo
        
        **Quy định trả lời:**
        - Công thức viết trong $...$ 
        - Ví dụ: $\\sqrt{{x + 1}}$, $\\int_a^b f(x) dx$
        - Không dùng ký tự đặc biệt ngoài LaTeX
        - Tối đa 5 bước cho mỗi phần giải
        - Mỗi bước không quá 2 dòng
        
        **Yêu cầu trả lời:**
        Trả lời dạng JSON với cấu trúc sau:
        {{
            "bot_response": "Nội dung trả lời cho học sinh",
            "stage_action": "stay|next|previous|goto:section_name",
            "tab_action": "lesson-content|examples|exercises|tools",
            "progress_update": số từ 0-100 nếu cần cập nhật tiến độ
        }}
        
        **Thông tin ngữ cảnh:**
        - Lịch sử chat gần nhất: 
        {conversation_history}
        '''
    
    def __init__(self, conversation_manager, lesson_data):
        self.conversation_manager = conversation_manager
        self.lesson_data = lesson_data
        
    def generate(self, user_input):
        # Get the current section based on the section index
        current_section = None
        if self.lesson_data and 'sections' in self.lesson_data:
            sections = self.lesson_data['sections']
            print(self.conversation_manager.section_index)
            if 0 <= self.conversation_manager.section_index < len(sections):
                print("yes")
                current_section = sections[self.conversation_manager.section_index]

        
        lesson_title = self.lesson_data.get('title', 'Unknown Lesson') if self.lesson_data else 'Unknown Lesson'
        total_sections = len(self.lesson_data['sections']) if self.lesson_data and 'sections' in self.lesson_data else 0
        current_section_title = current_section.get('title', 'Unknown Section') if current_section else 'None'

        print("lesson_title:", lesson_title)
        print("lesson_stage:", self.conversation_manager.lesson_stage)
        print("section_index:", self.conversation_manager.section_index + 1)
        print("total_sections:", total_sections)
        print("current_section_title:", current_section_title)
        print("conversation_history:", self.conversation_manager.get_formatted_history())

        return self.PROMPT_TEMPLATE.format(
            lesson_title=lesson_title,
            lesson_stage=self.conversation_manager.lesson_stage,
            section_index=self.conversation_manager.section_index + 1,
            total_sections=total_sections,
            current_section_title=current_section_title,
            conversation_history=self.conversation_manager.get_formatted_history(),
        )

class ResponseProcessor:
    @staticmethod
    def clean_response(raw_response):
        """Xử lý các ký tự đặc biệt và markdown artifacts"""
        cleaned = re.sub(r'```(json)?', '', raw_response)
        cleaned = cleaned.replace('\r\n', '\n').replace('\r', '\n')
        cleaned = re.sub(
            r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', 
            r'\\\\', 
            cleaned
        )
        return cleaned

    @staticmethod
    def parse_json_response(cleaned_response):
        """Xử lý và validate JSON response"""
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            start = cleaned_response.find('{')
            end = cleaned_response.rfind('}')
            if start != -1 and end != -1:
                return json.loads(cleaned_response[start:end+1])
            raise

    @staticmethod
    def process_content(content):
        """Chuyển đổi định dạng markdown sang HTML"""
        # Xử lý bullet points và số thứ tự
        content = re.sub(r'(\d+\.)\s', r'<span class="list-number">\1</span> ', content)
        content = re.sub(r'•\s', r'<span class="list-bullet">•</span> ', content)
        
        # Fix căn bậc 2
        content = re.sub(r'\\sqrt(\w+)', r'\\sqrt{\1}', content)
        
        # Xử lý in đậm với dấu **
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        
        # Thêm khoảng trắng sau dấu $
        content = re.sub(r'\$(?! )', '$ ', content)
        content = re.sub(r'(?<! )\$', ' $', content)
        
        # Xử lý thụt đầu dòng
        content = re.sub(r'\n\s{2,}', lambda m: '\n' + ' ' * (len(m.group(0))//2), content)
        
        # Thay thế các ký tự bullet đặc biệt
        bullet_replacements = {'◦': '○', '■': '▪', '‣': '▸'}
        for k, v in bullet_replacements.items():
            content = content.replace(k, v)
        
        return content
    
    @staticmethod
    def process_agent_actions(response_data, conversation_manager, lesson_data):
        """Process agent actions from the response"""
        actions = {
            'stage_change': False,
            'new_stage': None,
            'tab_change': False,
            'new_tab': None,
            'progress_update': False,
            'progress': None
        }
        
        # Process stage action
        stage_action = response_data.get('stage_action', 'stay')
        if stage_action != 'stay':
            actions['stage_change'] = True
            
            if stage_action == 'next':
                # Move to next section
                if conversation_manager.section_index < len(lesson_data.get('sections', [])) - 1:
                    conversation_manager.section_index += 1
                    actions['new_stage'] = 'section'
                else:
                    # If no more sections, move to conclusion
                    conversation_manager.lesson_stage = 'conclusion'
                    actions['new_stage'] = 'conclusion'
            
            elif stage_action == 'previous':
                # Move to previous section
                if conversation_manager.section_index > 0:
                    conversation_manager.section_index -= 1
                    actions['new_stage'] = 'section'
            
            elif stage_action.startswith('goto:'):
                # Go to a specific section by name
                target_section = stage_action.split(':', 1)[1]
                for i, section in enumerate(lesson_data.get('sections', [])):
                    if section.get('title', '').lower() == target_section.lower():
                        conversation_manager.section_index = i
                        actions['new_stage'] = 'section'
                        break
        
        # Process tab action
        tab_action = response_data.get('tab_action')
        if tab_action and tab_action in ['lesson-content', 'examples', 'exercises', 'tools']:
            actions['tab_change'] = True
            actions['new_tab'] = tab_action
        
        # Process progress update
        progress = response_data.get('progress_update')
        if progress is not None:
            try:
                progress_value = float(progress)
                if 0 <= progress_value <= 100:
                    actions['progress_update'] = True
                    actions['progress'] = progress_value
            except (ValueError, TypeError):
                pass
                
        return actions

def get_llm_response(user_input, request, lesson_id=None):
    # Get lesson data
    lesson_data = None
    if lesson_id:
        try:
            # Fetch lesson data from API or database
            response = api_lesson_detail(request, lesson_id)
            lesson_data = json.loads(response.content.decode('utf-8'))  # Extract JSON from JsonResponse
        except Exception as e:
            print(f"Error fetching lesson data: {e}")
            lesson_data = None
            
    # Initialize components
    conv_manager = ConversationManager(request.session)
    prompt_engine = PromptEngine(conv_manager, lesson_data)
    llm_client = LLMClient("gemini-2.0-flash")
    
    # Add user message to history
    conv_manager.add_message('user', user_input)
    
    try:
        # Generate and process response
        prompt = prompt_engine.generate(user_input)
        print("prompt: ", prompt)
        
        try:
            raw_response = llm_client.generate(prompt)
        except Exception as e:
            print(f"Error [{e.code}]: {str(e)}")
            if e.details:
                print(f"Details: {e.details}")
                
        print("raw_response: ", raw_response)
        cleaned_response = ResponseProcessor.clean_response(raw_response)
        response_data = ResponseProcessor.parse_json_response(cleaned_response)
        
        # Process content
        bot_response = ResponseProcessor.process_content(response_data.get("bot_response", ""))
        
        # Process agent actions
        actions = ResponseProcessor.process_agent_actions(response_data, conv_manager, lesson_data)
        
    except (json.JSONDecodeError, AttributeError) as e:
        # Error handling
        print(f"Error processing response: {e}")
        bot_response = "Xin lỗi, có lỗi xảy ra khi xử lý phản hồi"
        actions = {
            'stage_change': False,
            'tab_change': False,
            'progress_update': False
        }
    
    # Update conversation
    bot_res = re.search(r'"bot_response":\s*"([^"]+)"', raw_response)
    if bot_res:
        conv_manager.add_message('bot', bot_res.group(1))
    
    # Save to database
    ChatMessage.objects.create(
        user_message=user_input,
        bot_response=bot_response,
        conversation=None
    )
    
    # Return response with actions
    return {
        'response': bot_response,
        'stage_change': actions.get('stage_change', False),
        'new_stage': actions.get('new_stage'),
        'tab_change': actions.get('tab_change', False),
        'new_tab': actions.get('new_tab'),
        'progress_update': actions.get('progress_update', False),
        'progress': actions.get('progress')
    }

