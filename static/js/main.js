document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(uploadForm);
            const submitBtn = uploadForm.querySelector('button[type="submit"]');

            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Обработка...';

            try {
                const response = await fetch('/api/documents/analyze/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Ошибка сервера');
                }

                const data = await response.json();
                displayResults(data);

            } catch (error) {
                alert('Ошибка: ' + error.message);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Анализировать';
            }
        });
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="card">
            <div class="card-header">
                Результаты анализа: ${data.document.title}
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Слово</th>
                                <th>TF</th>
                                <th>IDF</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.results.map((result, index) => `
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${result.word}</td>
                                    <td>${result.tf.toFixed(5)}</td>
                                    <td>${result.idf.toFixed(5)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}
