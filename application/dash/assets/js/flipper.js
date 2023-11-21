function toArray(arraylike) {
    var array = new Array(arraylike.length);
    for (var i = 0, n = arraylike.length; i<n; i++)
        array[i] = arraylike[i];
    return array;
}
function getCard(arrow) {
    return arrow.parentNode.parentNode.parentNode;
}
function flipCard() {
    var card = getCard(this)
    card.classList.toggle('flip')
}
function getBodyCard(shield) {
    return shield.parentNode.parentNode.nextSibling.children[0];
}
function toggleBodyCard() {
    var bodycard = getBodyCard(this)
    bodycard.classList.toggle('hide')
    var card = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
    card.classList.toggle('small')
}
function toggleAllBodyCards() {
    const bodycards = toArray(document.getElementsByClassName('card-body'))
    bodycards.forEach( (bodycard) => bodycard.classList.toggle('hide'))
    const cards = toArray(document.getElementsByClassName('complete-card'))
    cards.forEach( (card) => card.classList.toggle('small'))
}

