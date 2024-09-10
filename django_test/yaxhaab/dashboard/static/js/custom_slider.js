$(function () {
    $(".numeric-slider-range").slider({
        range: true,
        min: 0,
        max: 100,
        slide: function (event, ui) {
            
            check_max= new Date(ui.values[1]).toISOString() !== $("#" + $(this).parent().attr("id") + "_max").val()
            $("#" + $(this).parent().attr("id") + "_max").val(new Date(ui.values[1]).toISOString() );
            check_min= new Date(ui.values[0]).toISOString() !== $("#" + $(this).parent().attr("id") + "_min").val()
            $("#" + $(this).parent().attr("id") + "_min").val(new Date(ui.values[0]).toISOString() );
            new_text_min = (new Date(ui.values[0] ).toLocaleString())
            new_text_max = (new Date(ui.values[1] ).toLocaleString())
            if (check_max) {
                console.log("max_trigger")
                Unicorn.trigger("proyectMapeventListReactive", "slider_max");
            }
            if (check_min) {
                console.log("min_trigger")
                Unicorn.trigger("proyectMapeventListReactive", "slider_min");
            }
            $("#" + $(this).parent().attr("id") + "_text").text( new_text_min + " - " + new_text_max);
        },
        create: function (event, ui) {
            $(this).slider("option", 'min', (Date.parse($("#" + $(".numeric-slider").attr("id") + "_range_min").data("range_min")) ) );
            $(this).slider("option", 'max', (Date.parse($("#" + $(".numeric-slider").attr("id") + "_range_max").data("range_max")) ) );
            $(this).slider("option", 'values', [
                ((Date.parse($("#" + $(".numeric-slider").attr("id") + "_cur_min").text()))), 
                ((Date.parse($("#" + $(".numeric-slider").attr("id") + "_cur_max").text())))
            ]);
        }
    });
    $("#" + $(".numeric-slider").attr("id") + "_min").val(new Date($("#" + $(".numeric-slider").attr("id") + "_cur_min").text() ).toISOString());
    $("#" + $(".numeric-slider").attr("id") + "_max").val(new Date($("#" + $(".numeric-slider").attr("id") + "_cur_max").text() ).toISOString());
    $("#" + $(".numeric-slider").attr("id") + "_text").text((new Date($("#" + $(".numeric-slider").attr("id") + "_cur_min").text() )).toLocaleString() + 
    ' - ' + 
    (new Date($("#" + $(".numeric-slider").attr("id") + "_cur_max").text() )).toLocaleString());
});
