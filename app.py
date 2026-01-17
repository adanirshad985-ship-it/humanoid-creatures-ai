<!DOCTYPE html>
<html lang="ur">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal AI Image Editor</title>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #0f172a; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 2rem; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 90%; max-width: 500px; text-align: center; }
        h1 { color: #38bdf8; margin-bottom: 10px; }
        
        /* Upload Area */
        .upload-box { border: 2px dashed #38bdf8; border-radius: 15px; padding: 20px; margin-bottom: 20px; cursor: pointer; transition: 0.3s; }
        .upload-box:hover { background: #334155; }
        #preview-img { max-width: 100%; border-radius: 10px; margin-top: 10px; display: none; }

        /* Input Styles */
        input[type="text"] { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; box-sizing: border-box; margin-bottom: 15px; }
        button { background: #38bdf8; color: #0f172a; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; transition: 0.3s; }
        button:hover { background: #0ea5e9; transform: translateY(-2px); }

        .loading { display: none; color: #fbbf24; margin-top: 10px; font-style: italic; }
    </style>
</head>
<body>

<div class="card">
    <h1>AI Custom Editor</h1>
    <p>Apni image upload karein aur tabdeeli likhein</p>

    <div class="upload-box" onclick="document.getElementById('fileInput').click()">
        <span id="uploadText">📁 Click to Upload Image</span>
        <input type="file" id="fileInput" accept="image/*" style="display: none;">
        <img id="preview-img" src="#" alt="Preview">
    </div>

    <input type="text" id="promptInput" placeholder="E.g. Change dress to Red Armor, add a lion, change skin to blue">
    
    <button id="generateBtn">Magic Process ✨</button>

    <div class="loading" id="loader">AI is working on your request...</div>
    <div id="result-status" style="margin-top: 20px; color: #10b981;"></div>
</div>

<script>
    const fileInput = document.getElementById('fileInput');
    const previewImg = document.getElementById('preview-img');
    const uploadText = document.getElementById('uploadText');
    const generateBtn = document.getElementById('generateBtn');
    const loader = document.getElementById('loader');

    // 1. Image Preview Logic
    fileInput.onchange = evt => {
        const [file] = fileInput.files;
        if (file) {
            previewImg.src = URL.createObjectURL(file);
            previewImg.style.display = 'block';
            uploadText.style.display = 'none';
        }
    }

    // 2. API Connection Logic
    generateBtn.onclick = async () => {
        const prompt = document.getElementById('promptInput').value;
        const apiKey = "YOUR_GEMINI_API_KEY"; // <-- Apni Key Yahan Lagayein

        if (!fileInput.files[0] || !prompt) {
            alert("Pehle image select karein aur phir batayein kya change karna hai!");
            return;
        }

        loader.style.display = 'block';
        generateBtn.disabled = true;

        try {
            // Note: Gemini API image handling ke liye base64 conversion zaroori hoti hai
            // Yeh fetch call aapki web app ko Gemini 3 Flash/Pro se connect karega
            console.log("Sending to AI with prompt: " + prompt);
            
            // Abhi ke liye hum status dikha rahe hain, aap yahan API call likhenge
            setTimeout(() => {
                loader.style.display = 'none';
                generateBtn.disabled = false;
                document.getElementById('result-status').innerText = "Personal AI has processed the request! (API response code goes here)";
            }, 3000);

        } catch (error) {
            alert("Error: " + error.message);
            loader.style.display = 'none';
            generateBtn.disabled = false;
        }
    };
</script>

</body>
</html>
