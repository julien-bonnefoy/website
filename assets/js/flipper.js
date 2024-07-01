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
    return shield.parentElement.parentElement.childNodes[5].childNodes[1];
}
function getBackBodyCard(shield) {
    return shield.parentElement.parentElement.nextElementSibling.childNodes[5];
}
function toggleBodyCard() {
    var bodycard = getBodyCard(this)
    bodycard.classList.toggle('hide')
    var bbodycard = getBackBodyCard(this)
    bbodycard.classList.toggle('hide')
    var complete = this.parentElement.parentElement.parentElement.parentElement.parentElement
    complete.classList.toggle('small')
}
function toggleAllBodyCards() {
    const bodycards = toArray(document.getElementsByClassName('card-body'))
    bodycards.forEach( (bodycard) => bodycard.classList.toggle('hide'))
    const cards = toArray(document.getElementsByClassName('complete-card'))
    cards.forEach( (card) => card.classList.toggle('small'))
}
function changeTooltip() {
    const tooltipsRight = toArray(document.getElementsByClassName('leaflet-tooltip-right'))
    if (tooltipsRight.length > 0) {
        tooltipsRight[0].classList = "leaflet-tooltip-pane leaflet-tooltip-top"
    }
    const tooltipsLeft = toArray(document.getElementsByClassName('leaflet-tooltip-left'))
    if (tooltipsLeft.length > 0) {
        tooltipsLeft[0].classList = "leaflet-tooltip-pane leaflet-tooltip-top"
    }
}