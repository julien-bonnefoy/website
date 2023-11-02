$(document).ready(function () {
    var frameElement = document.getElementById('dash-frame')
    var doc = frameElement.contentDocument;
    var head = doc.head;
    var link1 = doc.createElement('link');
    link1.type = 'text/css'
    link1.rel = 'stylesheet'
    link1.href = 'https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css'
    head.appendChild(link1);
    var link2 = doc.createElement('link');
    link2.type = 'text/javascript'
    link2.rel = 'script'
    link1.href = 'https://code.jquery.com/jquery-3.7.0.js'
    head.appendChild(link2);
    var link3 = doc.createElement('link');
    link3.type = 'text/javascript'
    link3.rel = 'script'
    link3.href = 'https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js'
    head.appendChild(link3);
    console.log('ok');
    })