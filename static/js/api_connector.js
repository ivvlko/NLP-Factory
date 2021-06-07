const base_url = 'http://127.0.0.1:5000/api/';
const dynamicTag = document.getElementsByClassName('main-container')[0];
const btns = document.getElementsByClassName('categories-link');


for (let i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', loadJsonData);
}

function loadJsonData(e) {
    const target = e.target.innerHTML;
    fetch(base_url)
        .then(res => res.json())
        .then(data => {
            let latestSix = [];
            for (let i = 0; i < data.length; i++) {
                if (latestSix.length === 20) {
                    break
                }
                if (data[i].standard_ml_label === target) {
                    latestSix.push(data[i]);
                }
            }
            let finalTemplate = changeTemplateDynamically(latestSix);
            dynamicTag.innerHTML = finalTemplate;
        })
}

function changeTemplateDynamically(d) {
    let result = ``;
    for (let i = 0; i < d.length; i++) {
        let current = `
            <section class="content">
                    <div class="content-data-title" style="color: pink; font-size: 150%">${d[i].title}</div>
                    <div class="content-data-txt">${d[i].raw_txt}</div>
                    
                    <p class="content-data" style="color: wheat">ML label: ${d[i].standard_ml_label}</p>
            </section>`
        result += current;
    }
    return result
}

