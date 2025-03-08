// Biến theo dõi trạng thái bài học
let currentLesson = {
    id: 1, // Default lesson ID
    name: "Bài 1: Tính đơn điệu và cực trị của hàm số",
    stage: "opening", // opening, start, learn, practice, end
    topic: 0,
    progress: 10,
    completedSections: []
};

// Initialize CSRF token for AJAX requests
const csrftoken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

// Function to send chat message
document.addEventListener('DOMContentLoaded', function() {
    // Get lesson ID from URL before using it
    currentLesson.id = getLessonIdFromUrl();

    // Fetch and load lesson content
    fetchLessonInfo(currentLesson.id);
    loadLessonContent(currentLesson.id);

    // Set up event listeners
    const input = document.getElementById('message-input');
    input.addEventListener('input', autoResizeTextarea);

    // Add default message in chat and send it automatically
    sendMessage("Bắt đầu bài học");
});


// Function to extract the lesson ID from the URL
function getLessonIdFromUrl() {
    const urlPath = window.location.pathname;
    const pathSegments = urlPath.split('/');
    return pathSegments[pathSegments.length - 2];
}

// Function to load all lesson content
function loadLessonContent(lessonId) {
    // Load all lesson data in a single API call
    axios.get(`/lessons/api/${lessonId}/`)
        .then(response => {
            const data = response.data;
            // Update lesson state
            currentLesson.name = data.title;
            currentLesson.progress = data.progress;
            currentLesson.stage = data.stage;
            currentLesson.topic = data.topic;
            currentLesson.completedSections = data.completed_sections;
            
            // Update UI
            document.getElementById('lesson-status').textContent = data.title;
            document.querySelector('.section-title').textContent = data.title;
            updateProgressBar();
            
            // Render all content
            renderLessonContent(data);
            renderExamples(data.sections);
            renderExercises(data.sections);
            renderTools(data);
            
            // Add welcome message if needed
            if (data.welcome_message && document.querySelectorAll('.message').length <= 1) {
                addMessage('assistant', data.welcome_message);
            }
        })
        .catch(error => {
            console.error('Error fetching lesson content:', error);
            document.getElementById('lesson-dynamic-content').innerHTML = 
                '<div class="error-message">Không thể tải nội dung bài học. Vui lòng thử lại sau.</div>';
        });
}

// Function to render lesson content
function renderLessonContent(lessonData) {
    const container = document.getElementById('lesson-dynamic-content');
    
    // Clear previous content
    container.innerHTML = '';
    
    // Add lesson description
    const descriptionDiv = document.createElement('div');
    descriptionDiv.className = 'subsection fade-in';
    descriptionDiv.innerHTML = `
        <div class="subsection-title">${lessonData.title}</div>
        <p>${lessonData.description}</p>
    `;
    container.appendChild(descriptionDiv);
    
    // Sort sections by order
    const sortedSections = lessonData.sections.sort((a, b) => a.order - b.order);
    
    // Add each section
    sortedSections.forEach(section => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'subsection fade-in';
        sectionDiv.innerHTML = `
            <div class="subsection-title">${section.title}</div>
            <div class="section-content">${section.content}</div>
        `;
        container.appendChild(sectionDiv);
    });
}

// Function to render examples
function renderExamples(sections) {
    const container = document.getElementById('examples-dynamic-content');
    
    // Clear previous content
    container.innerHTML = '';
    
    // Collect all examples from all sections
    let allExamples = [];
    sections.forEach(section => {
        if (section.examples && section.examples.length > 0) {
            allExamples = allExamples.concat(section.examples);
        }
    });
    
    if (allExamples.length === 0) {
        container.innerHTML = '<div class="info-message">Chưa có ví dụ cho bài học này.</div>';
        return;
    }
    
    // Render all examples
    allExamples.forEach(example => {
        const exampleDiv = document.createElement('div');
        exampleDiv.className = 'example-item';
        
        let content = `<div class="explanation">${example.explanation}</div>`;
        if (example.image) {
            content += `<img src="${example.image}" alt="Example illustration" class="example-image">`;
        }
        
        exampleDiv.innerHTML = content;
        container.appendChild(exampleDiv);
    });
}

// Function to render exercises
function renderExercises(sections = []) {
    const container = document.getElementById('exercises-dynamic-content');
    if (!container) return;
    
    // Clear previous content
    container.innerHTML = '';
    
    // Check if sections exists and is an array
    if (!Array.isArray(sections)) {
        container.innerHTML = '<div class="info-message">Chưa có bài tập cho bài học này.</div>';
        return;
    }
    
    // Collect all exercises from all sections
    let allExercises = [];
    sections.forEach(section => {
        if (section && section.exercises && Array.isArray(section.exercises)) {
            allExercises = allExercises.concat(section.exercises);
        }
    });
    
    if (allExercises.length === 0) {
        container.innerHTML = '<div class="info-message">Chưa có bài tập cho bài học này.</div>';
        return;
    }
    
    // Render all exercises
    allExercises.forEach(exercise => {
        if (!exercise) return;
        
        const exerciseDiv = document.createElement('div');
        exerciseDiv.className = 'exercise-item';
        exerciseDiv.innerHTML = `
            <div class="question">${exercise.question || ''}</div>
            <div class="answer" id="answer-${exercise.id}" class="hidden">${exercise.answer || ''}</div>
            <button onclick="toggleAnswer(${exercise.id})">Hiển thị đáp án</button>
        `;
        container.appendChild(exerciseDiv);
    });
}

// Function to toggle exercise answer visibility
function toggleAnswer(index) {
    const answerElem = document.getElementById(`answer-${index}`);
    const button = event.target;
    
    if (answerElem.classList.contains('hidden')) {
        answerElem.classList.remove('hidden');
        button.textContent = 'Ẩn đáp án';
    } else {
        answerElem.classList.add('hidden');
        button.textContent = 'Hiển thị đáp án';
    }
}

// Function to render tools
function renderTools(lesson = {}) {
    const container = document.getElementById('tools-dynamic-content');
    if (!container) return;
    
    // Clear previous content
    container.innerHTML = '';
    
    // Tools are directly related to lesson, not sections
    const tools = lesson.tools && Array.isArray(lesson.tools) ? lesson.tools : [];
    
    if (tools.length === 0) {
        container.innerHTML = '<div class="info-message">Chưa có công cụ cho bài học này.</div>';
        return;
    }
    
    // Render all tools
    tools.forEach(tool => {
        if (!tool) return;
        
        const toolDiv = document.createElement('div');
        toolDiv.className = 'tool-item';
        let content = `
            <h3>${tool.name || ''}</h3>
            <p>${tool.description || ''}</p>
        `;
        if (tool.embed_url) {
            content += `<iframe src="${tool.embed_url}" frameborder="0"></iframe>`;
        }
        toolDiv.innerHTML = content;
        container.appendChild(toolDiv);
    });
}

// Function to initialize calculator
function initializeCalculator() {
    const calculator = document.querySelector('.calculator');
    const display = calculator.querySelector('.calculator-display');
    const keys = calculator.querySelector('.calculator-keys');
    
    let displayValue = '0';
    let firstValue = null;
    let operator = null;
    let waitingForSecondValue = false;
    
    keys.addEventListener('click', e => {
        const key = e.target;
        const action = key.classList.contains('calculator-key') ? key : null;
        
        if (!action) return;
        
        if (key.classList.contains('key-number')) {
            const keyValue = key.textContent;
            
            if (displayValue === '0' || waitingForSecondValue) {
                displayValue = keyValue;
                waitingForSecondValue = false;
            } else {
                displayValue = displayValue === '0' ? keyValue : displayValue + keyValue;
            }
        }
        
        if (key.classList.contains('key-decimal')) {
            if (!displayValue.includes('.')) {
                displayValue += '.';
            }
        }
        
        if (key.classList.contains('key-clear')) {
            displayValue = '0';
            firstValue = null;
            operator = null;
            waitingForSecondValue = false;
        }
        
        if (key.classList.contains('key-sign')) {
            displayValue = String(-parseFloat(displayValue));
        }
        
        if (key.classList.contains('key-percent')) {
            displayValue = String(parseFloat(displayValue) / 100);
        }
        
        if (key.classList.contains('key-operation')) {
            const operation = key.textContent;
            
            if (firstValue === null) {
                firstValue = parseFloat(displayValue);
            } else if (operator) {
                const result = calculate(firstValue, parseFloat(displayValue), operator);
                displayValue = String(result);
                firstValue = result;
            }
            
            waitingForSecondValue = true;
            operator = operation;
        }
        
        if (key.classList.contains('key-equals')) {
            if (firstValue === null) {
                return;
            }
            
            if (operator) {
                const secondValue = parseFloat(displayValue);
                displayValue = String(calculate(firstValue, secondValue, operator));
                firstValue = null;
                operator = null;
                waitingForSecondValue = false;
            }
        }
        
        display.textContent = displayValue;
    });
    
    function calculate(a, b, operation) {
        switch (operation) {
            case '+':
                return a + b;
            case '-':
                return a - b;
            case '×':
                return a * b;
            case '÷':
                return a / b;
            default:
                return b;
        }
    }
    
    // Add number class to number keys
    const numberKeys = calculator.querySelectorAll('.key-0, .key-1, .key-2, .key-3, .key-4, .key-5, .key-6, .key-7, .key-8, .key-9');
    numberKeys.forEach(key => key.classList.add('key-number'));
}


// Modify sendMessage to accept default messages
function sendMessage(defaultMessage = null) {
    const input = document.getElementById('message-input');
    let message = defaultMessage ? defaultMessage : input.value.trim();
    
    if (!message) return;

    // Add user message to chat
    addMessage('user', message);

    // Clear input only if it's not the default message
    if (!defaultMessage) {
        input.value = '';
        input.style.height = 'auto';
    }

    // Create FormData correctly
    const formData = new FormData();
    formData.append('lesson_id', currentLesson.id);
    formData.append('message', message);

    // Send message to backend
    axios.post('/chatbot/api/get_response/', 
        formData,
        {
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }
    )
    .then(response => {
        // Add assistant response to chat
        addMessage('assistant', response.data.response);
        
        // Check if we need to update the lesson content
        if (response.data.update_lesson) {
            updateLessonStage(response.data.new_stage);
        }
        
        // Check if we need to update the tab
        if (response.data.update_tab) {
            switchTab(response.data.new_tab);
        }
        
        // Check if we need to update the progress
        if (response.data.update_progress) {
            currentLesson.progress = response.data.progress;
            updateProgressBar();
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
        addMessage('assistant', 'Xin lỗi, tôi không thể xử lý tin nhắn của bạn lúc này. Vui lòng thử lại sau.');
    });
}


// Function to add message to chat
function addMessage(sender, text) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = formatMessageContent(text);
    chatMessages.appendChild(messageDiv);
    
    // Kích hoạt render LaTeX
    if (MathJax.typeset) {
        MathJax.typeset([messageDiv]);
    }
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessageContent(content) {

    // Xử lý căn bậc 2
    content = content.replace(/\\sqrt{([^}]+)}/g, '\\sqrt{$1}');

    // Xử lý in đậm
    content = content.replace(/<strong>(.*?)<\/strong>/g, '<strong>$1</strong>');
    
    // Kích hoạt MathJax render
    if (MathJax.typeset) {
        MathJax.typesetPromise().then(() => {
            // Fix căn chỉnh sau render
            document.querySelectorAll('.mjx-sqrt').forEach(sqrt => {
                sqrt.style.verticalAlign = 'middle';
            });
        });
    }
    // Xử lý thụt đầu dòng
    content = content.replace(/ /g, '<span class="indent"></span>');
    
    // Xử lý xuống dòng
    content = content.replace(/\n/g, '<br>');
    
    // Xử lý danh sách
    content = content.replace(/<span class="list-number">(\d+\.)<\/span>/g, '<span class="list-number">$1</span>');
    content = content.replace(/<span class="list-bullet">•<\/span>/g, '<span class="list-bullet">•</span>');
    
    // Xử lý LaTeX
    content = content.replace(/\$\$(.*?)\$\$/g, '<div class="latex-block">\\[$1\\]</div>');
    content = content.replace(/\$(.*?)\$/g, '<span class="latex-inline">\\($1\\)</span>');
    
    return content;
}

// Function to auto-resize textarea
function autoResizeTextarea() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    
    // Limit max height
    if (this.scrollHeight > 120) {
        this.style.height = '120px';
        this.style.overflowY = 'auto';
    } else {
        this.style.overflowY = 'hidden';
    }
}

// Handle Enter key in textarea
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Function to update lesson stage
function updateLessonStage(newStage) {
    currentLesson.stage = newStage;
    
    // Update UI based on stage
    switch (newStage) {
        case 'opening':
            document.getElementById('lesson-dynamic-content').innerHTML = lessonContent.opening.content;
            break;
        case 'start':
            document.getElementById('lesson-dynamic-content').innerHTML = lessonContent.start.content;
            break;
        case 'learn':
            // If we have a topic number, show that specific topic
            if (currentLesson.topic < lessonContent.learn.length) {
                document.getElementById('lesson-dynamic-content').innerHTML = 
                    lessonContent.learn[currentLesson.topic].content;
            }
            break;
        case 'practice':
            document.getElementById('lesson-dynamic-content').innerHTML = lessonContent.practice.content;
            switchTab('exercises');
            break;
        case 'end':
            document.getElementById('lesson-dynamic-content').innerHTML = lessonContent.end.content;
            break;
    }
    
    // Reload all other content
    loadLessonContent(currentLesson.id);
}

// Function to update progress bar
function updateProgressBar() {
    const progressFill = document.querySelector('.progress-fill');
    progressFill.style.width = `${currentLesson.progress}%`;
}

// Function to switch tabs
function switchTab(tabId) {
    // Hide all tab content
    document.getElementById('lesson-content').classList.add('hidden');
    document.getElementById('examples').classList.add('hidden');
    document.getElementById('exercises').classList.add('hidden');
    document.getElementById('tools').classList.add('hidden');
    
    // Show selected tab
    document.getElementById(tabId).classList.remove('hidden');
    
    // Update active tab
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Find and mark selected tab
    tabs.forEach(tab => {
        if (tab.getAttribute('onclick').includes(tabId)) {
            tab.classList.add('active');
        }
    });
    
    // Update lesson status with chat API
    axios.post('/chatbot/api/tab_change/', {
        lesson_id: currentLesson.id,
        tab: tabId
    })
    .then(response => {
        if (response.data.message) {
            addMessage('assistant', response.data.message);
        }
    })
    .catch(error => {
        console.error('Error updating tab:', error);
    });
}

// Function to toggle fullscreen for notebook
function toggleFullscreen() {
    const mainContainer = document.querySelector('.main-container');
    const chatSection = document.querySelector('.chat-section');
    const canvasSection = document.querySelector('.canvas-section');
    
    if (canvasSection.style.flex === '3' || canvasSection.classList.contains('fullscreen')) {
        // Exit fullscreen
        canvasSection.style.flex = '';
        chatSection.style.display = '';
        canvasSection.classList.remove('fullscreen');
        document.querySelector('#toggle-fullscreen svg').innerHTML = `
            <path d="M8 3H5a2 2 0 0 0-2 2v3"></path>
            <path d="M21 8V5a2 2 0 0 0-2-2h-3"></path>
            <path d="M3 16v3a2 2 0 0 0 2 2h3"></path>
            <path d="M16 21h3a2 2 0 0 0 2-2v-3"></path>
        `;
    } else {
        // Enter fullscreen
        canvasSection.style.flex = '3';
        chatSection.style.display = 'none';
        canvasSection.classList.add('fullscreen');
        document.querySelector('#toggle-fullscreen svg').innerHTML = `
            <path d="M4 14h6m-6-4h6m4 0h6m-6 4h6"></path>
        `;
    }
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to plot function (for the graph tool)
function plotFunction() {
    const input = document.getElementById('function-input').value;
    if (!input) return;
    
    const graphDisplay = document.getElementById('graph-display');
    graphDisplay.innerHTML = '';
    
    // Create canvas
    const canvas = document.createElement('canvas');
    canvas.id = 'function-graph';
    canvas.width = 400;
    canvas.height = 300;
    graphDisplay.appendChild(canvas);
    
    try {
        // Simple function plotter using canvas
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw axes
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        ctx.lineTo(width, height / 2);
        ctx.moveTo(width / 2, 0);
        ctx.lineTo(width / 2, height);
        ctx.strokeStyle = '#888';
        ctx.stroke();
        
        // Create function from input
        const fn = new Function('x', `return ${input.replace(/\^/g, '**')}`);
        
        // Plot function
        ctx.beginPath();
        
        const scale = 20; // Scale factor
        let started = false;
        
        for (let px = 0; px < width; px++) {
            const x = (px - width / 2) / scale;
            try {
                const y = fn(x);
                const py = height / 2 - y * scale;
                
                if (!started) {
                    ctx.moveTo(px, py);
                    started = true;
                } else {
                    ctx.lineTo(px, py);
                }
            } catch (e) {
                // Skip points where function is undefined
            }
        }
        
        ctx.strokeStyle = '#2196F3';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Add function label
        ctx.fillStyle = '#000';
        ctx.font = '14px Arial';
        ctx.fillText(`f(x) = ${input}`, 10, 20);
        
    } catch (error) {
        graphDisplay.innerHTML = `
            <div class="error-message">
                Lỗi khi vẽ đồ thị: ${error.message}
            </div>
        `;
    }
}        
// Function to fetch lesson information from the API
function fetchLessonInfo(lessonId) {
    fetch(`/lessons/api/${lessonId}/`)
        .then(response => response.json())
        .then(data => {
            displayLessonInfo(data);
        })
        .catch(error => console.error('Error fetching lesson info:', error));
}

// Function to display lesson information in HTML
function displayLessonInfo(data) {
    const lessonContentElement = document.getElementById('lesson-dynamic-content');
    lessonContentElement.innerHTML = `
        <div class="subsection fade-in">
            <div class="subsection-title">${data.title}</div>
            <p>${data.description}</p>
            <h3>Progress: ${data.progress}%</h3>
            ${data.sections.map(section => `
                <div class="section">
                    <h4>${section.title}</h4>
                    <p>${section.content}</p>
                    <h5>Examples</h5>
                    <ul>${section.examples.map(example => `
                        <li>
                            <p>${example.explanation}</p>
                            ${example.image ? `<img src="${example.image}" alt="Example Image">` : ''}
                        </li>`).join('')}
                    </ul>
                    <h5>Exercises</h5>
                    <ul>${section.exercises.map(exercise => `
                        <li>
                            <p>Question: ${exercise.question}</p>
                            <p>Answer: ${exercise.answer}</p>
                        </li>`).join('')}
                    </ul>
                </div>
            `).join('')}
        </div>
    `;
}

// Get CSRF token from cookie
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
