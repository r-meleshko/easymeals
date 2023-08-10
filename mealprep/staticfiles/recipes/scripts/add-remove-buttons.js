/*
Add/remove buttons for Choose, Active and Favorite views.
If recipe is added to active, change card border to green. If added to favorite, display green star on the card's photo.
If recipe is removed from active/favorite on Active/Favorite view, hide recipe's card.
Log changes to the model through /favorite_active_update route.
*/
$(document).ready(function () {
  $("[data-id='add_to_active'], [data-id='remove_from_active'], [data-id='add_to_favorites'], [data-id='remove_from_favorites']").click(function (event) {
    var page_type = $(this).attr("data-page-type");
    var recipe_id = $(this).attr("data-recipe-id");
    var operation_type = $(this).attr("data-id");
    $.post({
        url: "/favorite_active_update",
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        'data': {
            'action': operation_type.split('_')[0],
            'model': operation_type.split('_')[2],
            'recipe_id': recipe_id,
        },
        success: function ( data ) {
            if (operation_type == "add_to_active") {
                $('[data-id="card_' + recipe_id + '"]').attr("class", "card shadow-sm h-100 border border-2 border-success");
                $('[data-id="div_add_to_active_' + recipe_id + '"]').hide();
                $('[data-id="div_remove_from_active_' + recipe_id + '"]').show();
            } else if (operation_type == "remove_from_active") {
                if (page_type == 'active') {
                    $('[data-id="col_' + recipe_id + '"]').hide();
                } else {
                    $('[data-id="card_' + recipe_id + '"]').attr("class", "card shadow-sm h-100");
                    $('[data-id="div_add_to_active_' + recipe_id + '"]').show();
                    $('[data-id="div_remove_from_active_' + recipe_id + '"]').hide();
                }
            } else if (operation_type == "add_to_favorites") {
                $('[data-id="div_add_to_favorites_' + recipe_id + '"]').hide();
                $('[data-id="div_remove_from_favorites_' + recipe_id + '"]').show();
                $('[data-id="favorite_star_' + recipe_id + '"]').show();
            } else if (operation_type == "remove_from_favorites") {
                if (page_type == 'favorites') {
                    $('[data-id="col_' + recipe_id + '"]').hide();
                } else {
                    $('[data-id="div_add_to_favorites_' + recipe_id + '"]').show();
                    $('[data-id="div_remove_from_favorites_' + recipe_id + '"]').hide();
                    $('[data-id="favorite_star_' + recipe_id + '"]').hide();
                }
                }
            }
        });
        return false;
  });
});
