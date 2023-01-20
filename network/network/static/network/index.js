function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

window.addEventListener('load', function () {
    this.document.querySelectorAll('.delete_btn').forEach((btn)=>{
        btn.addEventListener("click", ()=>{
            const request = new Request(
                '/',
                {
                    method: 'DELETE',
                    headers: {'X-CSRFToken': csrftoken},
                    mode: 'same-origin',
                    body: btn.value
                }
            );
            fetch(request)
            .then(response => response.json())
            .then(result => {
                
                if (result.action === "deleted"){
                    btn.parentNode.parentNode.removeChild(btn.parentNode)
                }
            });
        })
    })
    document.querySelectorAll('.like_btn').forEach((btn) =>{
        btn.addEventListener('click', ()=>{
            const request = new Request(
                '/',
                {
                    method: 'PUT',
                    headers: {'X-CSRFToken': csrftoken},
                    mode: 'same-origin',
                    body: btn.value
                }
            );
            fetch(request)
            .then(response => response.json())
            .then(result => {
                if (result.action === "login"){
                    window.location.href = "/login"
                }
                $(btn).find("div").load(document.URL+" ."+btn.classList[1]+" div")
            });  
        })
    })
  })

    
