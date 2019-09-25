moment.locale("en");
function flask_moment_render(elem) {
    elem.innerHTML = eval('moment("' + elem.dataset.timestamp + '").' + elem.dataset.format + ';');
    elem.classList.remove('flask-moment')
    elem.style.display = 'inline';
}
function flask_moment_render_all() {
    elems = Array.from(document.getElementsByClassName('flask-moment'));
    for (var i = 0; i < elems.length; i++) {
        elem = elems[i];
        flask_moment_render(elem);
        if (elem.dataset.refresh > 0) {
            setInterval(function() { flask_moment_render(this); }.bind(elem), parseInt(elem.dataset.refresh));
        }
    }
}
document.addEventListener('DOMContentLoaded', function() {
    flask_moment_render_all();
});
