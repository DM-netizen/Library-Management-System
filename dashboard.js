let limit = 5;
let pages = 1;



limit = document.getElementById("limit").value;
genre = document.getElementById("genre").value;
rating = document.getElementById("rating").value;

let url = `browse?page=${page}&limit=${limit}`

if(genre){
    url += `&genre=${genre}`
}

if(rating) {
    url += `&rating=${rating}`
}

const response = fetch(url);