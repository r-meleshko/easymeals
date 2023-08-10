// Filter recipes by meal type and by total preparation time.

// Style meal type and preparation time selection element.
$(document).ready(function(){
    var choose_meal_type = new Choices('#select-meal-type', {
        removeItemButton: true
    });
    $("#select-meal-type").css('visibility', 'visible');
});

$(document).ready(function(){
    var choose_prep_time = new Choices('#select-prep-time', {
        placeholder: true,
        placeholderValue: 'Max preparation time'
    });
    $("#select-prep-time").css('visibility', 'visible');
});


// Filters updating the page based on changes.
function MealTypeFilter() {
    $('[data-elem-type="recipe-card"]').attr('data-type-filter', 'hide');
    $('[data-type-filter="hide"]').hide();
    var meal_types = $('#select-meal-type').val();
    switch (meal_types.length) {
        case 0:
            $('[data-elem-type="recipe-card"]').attr('data-type-filter', 'show');
            $('[data-type-filter="show"][data-time-filter="show"]').show();
        default:
            for (const meal_type of meal_types) {
                $('[data-meal-type="' + meal_type + '"]').attr('data-type-filter', 'show');
                $('[data-type-filter="show"][data-time-filter="show"]').show();
        }
    };
};

function MealTimeFilter() {
    $('[data-elem-type="recipe-card"]').attr('data-time-filter', 'hide');
    $('[data-time-filter="hide"]').hide();
    var prep_time = $("#select-prep-time").val();
    $('[data-elem-type="recipe-card"]').filter(function(){
        return $(this).attr('data-prep-time') <= prep_time;
    }).attr('data-time-filter', 'show');
    $('[data-time-filter="show"][data-type-filter="show"]').show();
};


// Listener on selection change.
$(document).on("change", '#select-prep-time', function() {
    MealTimeFilter();
});

$(document).on("change", '#select-meal-type', function() {
    MealTypeFilter();
});

// Apply both filters on reload.
$(document).ready(function()  {
    MealTypeFilter();
    MealTimeFilter();
});
