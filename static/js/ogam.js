$(document).ready(function () {
    $(".box").click(function () {
        let isChecked = $(this).find('input').is(":checked");
        $(this).find('input').prop('checked', !isChecked);
        if (isChecked)
            $(this).css("border-color", "black");
        else
            $(this).css("border-color", "blue");

        let cntChecked = $('input:checkbox:checked').length;
        let str = "";
        if (cntChecked > 0)
            str = cntChecked + "개 선택됨";
        else
            str = "";
        $("#info").html(str);
    });
});