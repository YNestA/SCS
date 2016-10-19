/**
 * Created by yang on 16-10-7.
 */
function setTableBC() {
    $("#finish_table tbody tr:odd").css("background-color","#f6f4f0");
    $("#finish_table tbody tr:even").css("background-color","#fff");
}
$(document).ready(function () {
    $("#left_arrow").detach().appendTo($("#left ul li:eq(3)"));
    setTableBC();
});
