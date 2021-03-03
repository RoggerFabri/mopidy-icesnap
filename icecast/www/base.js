$(document).ready(function () {
    if ($("#playing-now").length) {
        $("#sleeping").hide();
    } else {
        $("#sleeping").show();
    }
});