$(function () {
    $(".numeric-slider-range").slider({
        range: true,
        min: 0,
        max: 100,
        slide: function (event, ui) {
            check_min= new Date(ui.values[0]).toISOString() !== $("#" + $(this).parent().attr("id") + "_min").val()
            if (check_min) {
                $("#" + $(this).parent().attr("id") + "_min").val(new Date(ui.values[0]).toISOString() );
                Unicorn.trigger("proyectMapeventListReactive", "slider_min");
            }
            check_max= new Date(ui.values[1]).toISOString() !== $("#" + $(this).parent().attr("id") + "_max").val()
            if (check_max) {
                $("#" + $(this).parent().attr("id") + "_max").val(new Date(ui.values[1]).toISOString() );
                Unicorn.trigger("proyectMapeventListReactive", "slider_max");
            }
            $("#" + $(this).parent().attr("id") + "_text").text((new Date(ui.values[0] ).toLocaleString()) + " - " + (new Date(ui.values[1] )).toLocaleString());
        },
        create: function (event, ui) {
            $(this).slider("option", 'min', (Date.parse($(this).parent().data("range_min")) ) );
            $(this).slider("option", 'max', (Date.parse($(this).parent().data("range_max")) ) );
            $(this).slider("option", 'values', [
                ((Date.parse($(this).parent().data("cur_min")))), 
                ((Date.parse($(this).parent().data("cur_max"))))
            ]);
        }
    });
    $("#" + $(".numeric-slider").attr("id") + "_min").val(new Date($(".numeric-slider").data("cur_min") ).toISOString());
    $("#" + $(".numeric-slider").attr("id") + "_max").val(new Date($(".numeric-slider").data("cur_max") ).toISOString());
    $("#" + $(".numeric-slider").attr("id") + "_text").text((new Date($(".numeric-slider").data("cur_min") )).toLocaleString() + 
    ' - ' + 
    (new Date($(".numeric-slider").data("cur_max") )).toLocaleString());
});
