$(document).ready(function () {
    error = ""
    function validate(keywords) {
        if (keywords.length > 3) {
            error = "Please type up to 3 keywords only. We don't want to hammer Google!"
            return false
        }
        return true
    }
    function send(data) {
        $.ajax({
            type: "post",
            url: "http://localhost/api/send",
            data: data,
            dataType: "json",
            beforeSend: function () {
                $("#spinner").show();
            },
            complete: function () {
                $("#spinner").hide();
            },
            success: function (response) {
                $("#success").show()
                $("#success").text(response)
            }
        });
    }
    $('button#submit').click(function () {
        var text = $('textarea#keywords').val();
        if (text == "") {
            alert("We need some keywords to get started!")
        } else {
            text_arr = text.split("\n");
            if (validate(text_arr)) {
                send(JSON.stringify({"keywords":text_arr}));
            } else {
                alert(error)
            }
        }
    });
});