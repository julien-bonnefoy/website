function toArray(arraylike) {
    var array= new Array(arraylike.length);
    for (var i= 0, n= arraylike.length; i<n; i++)
        array[i]= arraylike[i];
    return array;
}
function getCard(arrow) {
    return arrow.parentNode.parentNode.parentNode
}
function flipCard() {
    var card = getCard(this)
    card.classList.toggle('flip')
}
/* var frames = document.getElementsByTagName('iframe'); */
