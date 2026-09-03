// static/js/search.js
document.getElementById('searchBtn').addEventListener('click', performSearch);
document.getElementById('keywordInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') performSearch();
});

function performSearch() {
    const keyword = document.getElementById('keywordInput').value;
    const skill = document.getElementById('skillFilter').value;
    const jobTitle = document.getElementById('jobTitleFilter').value;
    const location = document.getElementById('locationFilter').value;

    // ساخت URL با پارامترها
    let url = `/api/search/?keyword=${encodeURIComponent(keyword)}`;
    if (skill) url += `&skill=${encodeURIComponent(skill)}`;
    if (jobTitle) url += `&job_title=${encodeURIComponent(jobTitle)}`;
    if (location) url += `&location=${encodeURIComponent(location)}`;

    // درخواست به API
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayResults(data.results);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('results').innerHTML =
                '<div class="alert alert-danger">خطا در ارتباط با سرور</div>';
        });
}

function displayResults(profiles) {
    const resultsDiv = document.getElementById('results');

    if (profiles.length === 0) {
        resultsDiv.innerHTML = '<div class="col-12 text-center text-muted">نتیجه‌ای یافت نشد</div>';
        return;
    }

    let html = '';
    profiles.forEach(profile => {
        html += `
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${profile.full_name}</h5>
                        <p class="card-text">
                            <strong>مکان:</strong> ${profile.location || 'نامشخص'}<br>
                            <strong>مهارت‌ها:</strong> ${profile.skills.join('، ')}<br>
                            <strong>سوابق شغلی:</strong> ${profile.experience.map(exp => exp.title).join('، ')}
                        </p>
                        <button class="btn btn-sm btn-outline-primary" onclick="showDetail('${profile.id}')">
                            مشاهده جزئیات
                        </button>
                    </div>
                </div>
            </div>
        `;
    });

    resultsDiv.innerHTML = html;
}

function showDetail(id) {
    // می‌تونی یه مودال برای جزئیات بیشتر بسازی
    alert(`جزئیات پروفایل با ID: ${id}`);
}