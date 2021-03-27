document.addEventListener('DOMContentLoaded', function() {
    // document.querySelector('#author_search_button').addEventListener('click', () => search());
    // document.querySelector('#writing_search_button').addEventListener('click', () => search());
    // document.querySelector('#search_button').addEventListener('click', () => search());

    // document.querySelector('#author_search').addEventListener('change', () => search());
    // document.querySelector('#writing_search').addEventListener('change', () => search());

    document.querySelector('#author_filter').addEventListener('change', () => filter());
    document.querySelector('#writing_filter').addEventListener('change', () => filter());
});

async function setSelectedGenre() {
    const genres = ['', 'Проза', 'Поэзия', 'Неизвестно']

    const select = document.querySelector('#genre');
    let post = {genre: genre.value};
	let response = await fetch('/pushkin/writing_set_selected_genre', {
		method: 'POST',
	    headers: {
        'Content-Type': 'application/json;charset=utf-8'
		},
		body: JSON.stringify(post)
	});
    console.log(response.status);
    if (response.status == '200') {
        const checkboxes = document.querySelectorAll(`.toggle_writing_active:checked`);
        for (let i = 0; i < checkboxes.length; i++) {
            wid = checkboxes[i].getAttribute('wid');
            document.querySelector(`[gid="${wid}"]`).innerHTML = genres[genre.value];
        }
    }
}

async function updateActiveCounts() {
    const active_a = document.querySelector('#active_a');
    const active_w = document.querySelector('#active_w');
    info = await fetch(`/pushkin/active_count`)
        .then (response => response.json());
    active_a.innerHTML = info.a_count;
    active_w.innerHTML = info.w_count;
}

async function toggleAuthorActive(id) {
    console.log('TAA', id);
    var result;
    var action;
	let post = {id: id, mode: ''};
	const checkbox = document.querySelector(`.toggle_author_active[aid="${id}"]`);
    if (checkbox.checked == true) {action = 'active'} else  {action = 'passive'};
	result = await fetch(`/pushkin/author_${action}`, {
		method: 'POST',
	    headers: {
        'Content-Type': 'application/json;charset=utf-8'
		},
		body: JSON.stringify(post)
	});
	console.log(result);
	updateActiveCounts();
}

async function writingsActive(id, active) {
    console.log('WA', id);
    var result;
    var action;
	let post = {id: id, mode: 'with_writings'};
	const checkbox = document.querySelector(`.toggle_author_active[aid="${id}"]`);
	const checkboxes = document.querySelectorAll(`.toggle_writing_active[aid="${id}"]`);
    if (active) {
        action = 'active'
        checkbox.checked= true;
        for (let i = 0; i < checkboxes.length; i++) {checkboxes[i].checked = true};
    } else {
        action = 'passive';
        checkbox.checked= false;
        for (let i = 0; i < checkboxes.length; i++) {checkboxes[i].checked = false};
    };
	result = await fetch(`/pushkin/author_${action}`, {
		method: 'POST',
	    headers: {
        'Content-Type': 'application/json;charset=utf-8'
		},
		body: JSON.stringify(post)
	});
	console.log(result);
	updateActiveCounts();
}

async function toggleWritingActive(id) {
	let post = {id: id};
	let response = await fetch('/pushkin/writing_check_active', {
		method: 'POST',
	    headers: {
        'Content-Type': 'application/json;charset=utf-8'
		},
		body: JSON.stringify(post)
	});
	updateActiveCounts();
}

// FILTER SEARCH

// async function search() {
//     const a_re = document.querySelector('#author_filter').value;
//     const w_re = document.querySelector('#writing_filter').value;
//     authors = document.querySelectorAll('.author');
//     const a_patt = new RegExp(a_re, "i");
//     const w_patt = new RegExp(w_re, "i");
//     for(var  i=0; i<authors.length; i++) {
//         var a_res = a_patt.test(authors[i].querySelector('name').innerHTML);
//         if (a_res) {
//             if (w_re != '') {authors[i].open = true;} else {authors[i].open = false;}
//             authors[i].style.display='block'
//             let found = false;
//             aid = authors[i].getAttribute('aid');
//             author_writings = document.querySelectorAll(`.writing[aid="${aid}"]`);
//             console.log(aid, author_writings.length);
//             for(var  j=0; j<author_writings.length; j++) {
//                 var w_res = w_patt.test(author_writings[j].querySelector('name').innerHTML);
//                 if (w_res) {
//                     found = true;
//                     author_writings[j].style.display = 'block';
//                 } else {
//                     author_writings[j].style.display = 'none';
//                 }
//             }
//             if (found) {
//                 authors[i].style.display='block';
//             } else {
//                 authors[i].open = false;
//                 if (w_re != '') {authors[i].style.display='none';}
//             }
//         }
//     }
// }

function show_all(list) {
    // console.log('show all ', list.length);
    for(var  f=0; f<list.length; f++) {
        list[f].style.display='block';
    }
}

function hide_all(list) {
    // console.log('hide all', list.length);
    for(var  f=0; f<list.length; f++) {
        list[f].style.display='none';
    }
}

function hide_dismatches(list, re) {
    // console.log('hide dismatches ', list.length, ' re: ', re)
    const patt = new RegExp(re, "i");
    for(var  f=0; f<list.length; f++) {
        var res = patt.test(list[f].querySelector('name').innerHTML);
        if (res) {
            list[f].style.display='block';
        } else {
            list[f].style.display='none';
        }
    }
}

function filter() {
	const a_f = document.getElementById('author_filter');
	const w_f = document.getElementById('writing_filter');

    authors = document.querySelectorAll('.author');
    writings = document.querySelectorAll('.writing');

    hide_dismatches(authors, a_f.value);
    hide_dismatches(writings, w_f.value);
}









