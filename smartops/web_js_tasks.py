import streamlit as st
from smartops.utils import show_page_header

def show_web_js_tasks():
    show_page_header("🌐 Web/JS Tasks")
    st.markdown("""
    ### Multi-Tool Web Utility
    - 📩 WhatsApp message sender
    - 📍 Location services
    - 🛒 Nearby grocery store finder
    - 🗺️ Route finder
    - 📸 Photo capture & download
    - 🎥 Video recording
    - 📧 Send text email
    - 📧 Send photo via email
    """)

    html_content = r"""
    <div style="padding:20px; font-family:Arial, sans-serif;">
        <!-- WhatsApp -->
        <div style="margin:20px 0; padding:15px; background:#f8f9fa; border-radius:6px;">
            <h3>&#128233; WhatsApp Message Sender</h3>
            <input type="text" id="whatsappMessage" placeholder="Type your message..." style="width:80%; padding:8px;">
            <button onclick="sendWhatsApp()" style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;">Send</button>
            <div id="whatsappStatus" style="margin-top:10px;color:#34B7F1;"></div>
        </div>

        <!-- Location -->
        <div style="margin:20px 0; padding:15px; background:#f8f9fa; border-radius:6px;">
            <h3>&#128205; Show My Location</h3>
            <button onclick="getLocation()" style="padding:8px 16px;">Get Location</button>
            <p id="locationOutput"></p>
        </div>

        <!-- Grocery -->
        <div style="margin:20px 0; padding:15px; background:#f8f9fa; border-radius:6px;">
            <h3>&#128722; Find Nearby Grocery Stores</h3>
            <button onclick="findGroceryStores()" style="padding:8px 16px;">Show Grocery Stores</button>
        </div>

        <!-- Route -->
        <div style="margin:20px 0; padding:15px; background:#f8f9fa; border-radius:6px;">
            <h3>&#128663; Route: Mansarovar to Sitapura</h3>
            <button onclick="openGoogleMapsRoute()" style="padding:8px 16px;">Show Directions</button>
        </div>

        <!-- Camera Photo -->
        <div style="margin:20px 0; padding:15px; background:#f8f9fa; border-radius:6px;">
            <h3>&#128247; Take a Photo</h3>
            <video id="videoCapture" width="320" height="240" autoplay style="border:1px solid black;"></video><br>
            <canvas id="canvasCapture" width="320" height="240" style="display:none;"></canvas><br>
            <button onclick="takePhoto()">Take Photo</button>
            <a id="downloadPhoto" style="display:none;">Download Photo</a>
        </div>

        <!-- Video Recording -->
        <div style="margin:20px 0; padding:15px; background:#f8f9fa; border-radius:6px;">
            <h3>&#127909; Record Video</h3>
            <video id="videoPreview" autoplay muted playsinline width="320"></video><br>
            <button onclick="startRecording()">Start Recording</button>
            <button onclick="stopRecording()">Stop Recording</button><br>
            <video id="videoPlayback" controls width="320"></video>
        </div>

        <!-- Text Email -->
        <div style="margin:20px 0; padding:15px; background:#f8f9fa; border-radius:6px;">
            <h3>&#128231; Send Text Email</h3>
            <form id="textEmailForm">
                <input type="text" name="from_name" placeholder="Your Name" required><br><br>
                <input type="email" name="reply_to" placeholder="Your Email" required><br><br>
                <textarea name="message" placeholder="Your Message" required></textarea><br><br>
                <button type="submit">Send Email</button>
            </form>
        </div>

        <!-- Photo Email -->
        <div style="margin:20px 0; padding:15px; background:#f8f9fa; border-radius:6px;">
            <h3>&#128247; Capture Photo & Send via Email</h3>
            <button onclick="startCameraForEmail()">Open Camera</button>
            <button id="snapBtnEmail" onclick="takePhotoForEmail()" style="display:none;">Take Photo</button>
            <canvas id="canvasEmail" width="320" height="240" style="display:none;"></canvas>
            <form id="emailForm" style="display:none;">
                <input type="hidden" name="from_name" value="Webcam User">
                <input type="hidden" name="reply_to" value="user@example.com">
                <input type="hidden" name="message" id="photoData">
                <button type="submit">Send Email with Photo</button>
            </form>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/emailjs-com@3/dist/email.min.js"></script>
    <script>
        emailjs.init("TMRkrarUmgfjdfh8t");

        // WhatsApp
        function sendWhatsApp(){
            const message=document.getElementById("whatsappMessage").value;
            const phone="919993917162";
            if(!message.trim()){ document.getElementById("whatsappStatus").innerText="Enter message"; return; }
            const url=`https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
            document.getElementById("whatsappStatus").innerText="Opening WhatsApp...";
            window.open(url);
        }

        // Location
        function getLocation(){
            if(navigator.geolocation){
                navigator.geolocation.getCurrentPosition(function(pos){
                    const lat=pos.coords.latitude, lon=pos.coords.longitude;
                    document.getElementById("locationOutput").innerHTML=
                        `Latitude: ${lat}<br>Longitude: ${lon}<br>
                        <a href="https://www.google.com/maps?q=${lat},${lon}" target="_blank">View on Google Maps</a>`;
                }, function(err){ alert("Error getting location: "+err.message); });
            }else{
                document.getElementById("locationOutput").innerText="Geolocation not supported.";
            }
        }

        // Grocery
        function findGroceryStores(){
            navigator.geolocation.getCurrentPosition(function(pos){
                const lat=pos.coords.latitude, lon=pos.coords.longitude;
                const url=`https://www.google.com/maps/search/grocery+store/@${lat},${lon},15z`;
                window.open(url,"_blank");
            }, function(err){ alert("Error: "+err.message); });
        }

        // Route
        function openGoogleMapsRoute(){
            window.open("https://www.google.com/maps/dir/Mansarovar,+Jaipur/Sitapura,+Jaipur", "_blank");
        }

        // Camera Photo
        const videoCapture=document.getElementById("videoCapture");
        const canvasCapture=document.getElementById("canvasCapture");
        const downloadPhoto=document.getElementById("downloadPhoto");
        let streamCapture;
        navigator.mediaDevices.getUserMedia({video:true}).then(s=>{ videoCapture.srcObject=s; streamCapture=s; }).catch(e=>alert(e));
        function takePhoto(){
            const ctx=canvasCapture.getContext("2d");
            ctx.drawImage(videoCapture,0,0,canvasCapture.width,canvasCapture.height);
            const dataURL=canvasCapture.toDataURL("image/png");
            downloadPhoto.href=dataURL; downloadPhoto.download="photo.png"; downloadPhoto.style.display="inline";
        }

        // Video Recording
        let mediaRecorder, recordedChunks=[];
        async function startRecording(){
            const stream = await navigator.mediaDevices.getUserMedia({video:true,audio:true});
            document.getElementById("videoPreview").srcObject=stream;
            recordedChunks=[];
            mediaRecorder=new MediaRecorder(stream);
            mediaRecorder.ondataavailable=e=>{ if(e.data.size>0) recordedChunks.push(e.data); };
            mediaRecorder.onstop=()=>{
                const blob=new Blob(recordedChunks,{type:'video/webm'});
                const url=URL.createObjectURL(blob);
                document.getElementById("videoPlayback").src=url;
                const a=document.createElement("a");
                a.href=url; a.download="video.webm"; a.click();
                stream.getTracks().forEach(track=>track.stop());
            };
            mediaRecorder.start();
            alert("Recording started");
        }
        function stopRecording(){ if(mediaRecorder && mediaRecorder.state!=="inactive") mediaRecorder.stop(); }

        // Text Email
        document.getElementById("textEmailForm").addEventListener("submit",function(e){
            e.preventDefault(); emailjs.sendForm("service_xtffw0u","template_p9cu2dq",this)
            .then(()=>alert("Text email sent")).catch(err=>alert("Failed: "+JSON.stringify(err)));
        });

        // Photo Email
        const canvasEmail=document.getElementById("canvasEmail");
        const photoDataInput=document.getElementById("photoData");
        const formEmail=document.getElementById("emailForm");
        const snapBtnEmail=document.getElementById("snapBtnEmail");
        let streamEmail;

        function startCameraForEmail(){
            navigator.mediaDevices.getUserMedia({video:true}).then(s=>{
                streamEmail=s; videoCapture.srcObject=streamEmail; videoCapture.style.display="block"; snapBtnEmail.style.display="inline";
            }).catch(err=>alert(err));
        }

        function takePhotoForEmail(){
            const ctx=canvasEmail.getContext("2d");
            ctx.drawImage(videoCapture,0,0,canvasEmail.width,canvasEmail.height);
            photoDataInput.value=canvasEmail.toDataURL("image/png");
            streamEmail.getTracks().forEach(track=>track.stop());
            videoCapture.style.display="none"; snapBtnEmail.style.display="none"; formEmail.style.display="block";
        }

        formEmail.addEventListener("submit",function(e){
            e.preventDefault();
            emailjs.sendForm("service_xtffw0u","template_p9cu2dq",this)
            .then(()=>alert("Email sent with photo")).catch(err=>alert("Failed: "+JSON.stringify(err)));
        });
    </script>
    """

    st.components.v1.html(html_content, height=1400, scrolling=True)
