const form_second = document.getElementById('upload-form-second');
const loading_second = document.getElementById('loading');
        form_second.addEventListener('submit', async (e) => {
            e.preventDefault();

            loading_second.style.display = 'block'; // Show loading
            const formData = new FormData(form_second);

            //Debug What beeing sent
            const data = {}
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }

            console.log(data)
            
            try {
                const response = await fetch('https://project-pdf-8ve3.onrender.com/MultipleUploadfiles/', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = data.file.name; // use correct filename
                    a.textContent = 'Download PDF';

                    document.getElementById('response_second').appendChild(a);
                }).catch(error => console.error('Error:', error));
                loading_second.style.display = 'none'; // Hide loading

            } catch (error) {
                console.error(error);
                document.getElementById('response').innerHTML = `Error uploading file`;
            }
        });