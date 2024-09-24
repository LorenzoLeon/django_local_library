$(function () {
    $(".numeric-slider-range").slider({
        range: true,
        min: 0,
        max: 100,
        slide: function (event, ui) {
            $("#" + $(this).parent().attr("id") + "_max").val(new Date(ui.values[1]).toISOString());
            $("#" + $(this).parent().attr("id") + "_min").val(new Date(ui.values[0]).toISOString());

            let new_text_min = (new Date(ui.values[0]).toLocaleDateString("en-GB").split(',')[0]);
            let new_text_max = (new Date(ui.values[1]).toLocaleDateString("en-GB").split(',')[0]);
            console.log(new_text_min)
            $("#" + $(this).parent().attr("id") + "_text").text(new_text_min + " - " + new_text_max);
        },
        create: function (event, ui) {
            var range_min = $("#" + $(".numeric-slider").attr("id") + "_range_min").data("range_min");
            var range_max = $("#" + $(".numeric-slider").attr("id") + "_range_max").data("range_max");
            $(this).slider("option", 'min', Date.parse(range_min));
            $(this).slider("option", 'max', Date.parse(range_max));
            $(this).slider("option", 'values', [Date.parse(range_min), Date.parse(range_max)]);
        }
    });

});
