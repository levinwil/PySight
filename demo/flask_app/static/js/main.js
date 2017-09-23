$(document).ready(function() {
    $("#execute_car").on("click", function(e) {
        uploadAndExecute("/car_no_car", $("#web_url").val());
    })
    $("#execute_text").on("click", function(e) {
        uploadAndExecute("/text", $("#web_url").val());
    })
    $("#execute_description").on("click", function(e) {
        uploadAndExecute("/description", $("#web_url").val());
    })
});


function uploadAndExecute(UPLOAD_URL, WEB_URL) {
    if (WEB_URL == "") {
        WEB_URL = "none";
    }
    $.ajax({
        url: UPLOAD_URL,
        method: "POST",
        data: {web_url: WEB_URL},
        success: function(data) {
            $("#text").val(data);
        },
    });
}
