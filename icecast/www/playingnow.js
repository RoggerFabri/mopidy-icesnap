var url = window.location.href + "status-json.xsl";

function getPlayingNowInformation(url) {
    $.getJSON(url)
        .fail(function (e) {
            console.log("Request failed!");
            setPlayingNow("...")
        })
        .done(function (response) {
            if (response) {
                if (response.server.streams.length == 0)
                    setPlayingNow("...")
                else {
                    var stream = response.server.streams[0];
                    setPlayingNow(stream.title)
                }
            }
        });
}

function setPlayingNow(info) {
    if (info.length == 0) {
        $("#playing-now").html("...")
    } else {
        $("#playing-now").html(info)
    }
}

$(document).ready(function () {
    if ($("#playing-now").length) {
        setInterval(function () {
            getPlayingNowInformation(url);
        }, 5000);
    } else {
        setTimeout(function () {
            window.location.reload(1);
        }, 15000);
    }
});