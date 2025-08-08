const loading = document.getElementById('loading');
const form = document.getElementById('upload-form-first');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            loading.style.display = 'block'; // Show loading
            const formData = new FormData(form);

            //Debug What beeing sent
            const data = {}
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }

            try {
                // http://127.0.0.1:8000/uploadfile/
                const response = await fetch('https://project-pdf-8ve3.onrender.com/uploadfile/', {
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

                    document.getElementById('response').appendChild(a);
                }).catch(error => console.error('Error:', error));
                loading.style.display = 'none'; // Hide loading

            } catch (error) {
                console.error(error);
                document.getElementById('response').innerHTML = `Error uploading file`;
            }
        });