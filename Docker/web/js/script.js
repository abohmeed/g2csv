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
            contentType: "application/json;charset=utf-8",
            beforeSend: function () {
                $("#spinner").show();
            },
            complete: function () {
                $("#spinner").hide();
            },
            success: function (response) {
                $("#success").show()
                if (response.Success){
                    $("#success").text("Lambda function successfully contacted. The CSV download link will appear in a few moments")
                    filename = response.Key + ".csv"
                    setTimeout(function(){
                        $("#download").show()
                        $("#download").attr("href", "https://s3-us-west-2.amazonaws.com/g2csv.downloads/" + filename);
                        $("#download").text("https://s3-us-west-2.amazonaws.com/g2csv.downloads/" + filename);
                    },5000)
                } else {
                    $("#failure").show()
                    $("#failure").text("Something wrong happened:" + response.Response)
                }
            }
        });
    }
    $('button#submit').click(function () {
        // Hide the message and the link
        $("#download").hide()
        $("success").hide()
        $("#failure").hide()
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