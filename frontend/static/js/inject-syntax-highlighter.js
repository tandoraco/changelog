function renderSyntaxHighlighter(value, index, array) {
    element_name = value[0]
    mode = value[1]
    element = document.getElementById(element_name)
    if(element) {
        element.style.border = '1px solid black';
        htmlMode = false;
        if(mode == 'xml') {
            htmlMode = true;
        }
        CodeMirror.fromTextArea(element, {
            lineNumbers: true, mode: {"name": mode, htmlMode: htmlMode}
        });
    }
}

function injectSyntaxHighlighter() {
  let elements = [
    ['id_javascript', 'javascript'],
    ['id_css', 'css'],
    ['id__settings', 'javascript'],
    ['id_plan_features', 'javascript'],
    ['id_template_content', 'xml'],
    ['id_extra_plan_features', 'javascript'],
  ]
  elements.map(renderSyntaxHighlighter);
}

window.onload = injectSyntaxHighlighter;