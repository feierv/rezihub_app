$(document).ready(function () {
    var selectedList = [];

    $('#learning-type-modal').on('hidden.bs.modal', function (e) {
        $("#start-learning-session-button").off("click");
    });

    const tabs = document.querySelectorAll('#learning-general-cateogries-navbar')

    function updateSubCategories(itemId) {
        let url = `/learning/chapter-select/${itemId}`

        $.get(url, function (data) {
            $('#sub-categories-container').html(data);
            attachSubCategoryClickHandlers();
        });
    }

    function checkExistingSessionHandler() {
        return new Promise(function(resolve, reject) {
            $.get(lastSessionURL, function(response) {
                if (response.exists == false) {
                    resolve(false);
                } else {
                    var session_id = response.exists.session_id;
                    resolve(session_id);
                }
            });
        });
    }

    function attachSubCategoryClickHandlers() {
        $('.subcategory__card').on('click', function () {
            var categoryId = $(this).data('category-id');
            const modal = $('#learning-type-modal')
            let sessionAlreadyExists;

            checkExistingSessionHandler().then(function(result) {
                if (result != false){
                    $('#return-to-progress').removeClass('hidden')
                    sessionAlreadyExists = result;
                } else {
                    $('#return-to-progress').addClass('hidden')
                }
            })
            
            .catch(function(error) {
                console.error('An error occurred:', error);
            });
           
            const closeModalButton = modal.find('#close-learning-modal')
            modal.modal('show');



            closeModalButton.click(function () {
                $('#learning-type-modal').modal('hide')
                $('.learning-option').removeClass('selected-learning-option');
                $('#page-number-container').addClass('hidden')
                $('.no-learning-option-selected').addClass('hidden')
            });

            $('#start-learning-session-button').on('click', function () {
                const selectedOption = $('.learning-option--selected').attr('id');

                if (selectedOption == 'page-number-order') {
                    if (selectedList.length > 0) {
                        const postData = {
                            learning_type: "page-number-order",
                            category_id: categoryId,
                            pages: selectedList,
                            csrfmiddlewaretoken: token // Include the CSRF token in your data
                        };
                        $.post(backendURL, postData, function (response) {
                            if (response.status === 200)
                            urlToRedirect = redirectURL.replace('0', response.session_id)
                            window.location.href = urlToRedirect
                        })
                            .fail(function (error) {
                                console.error('Error:', error);
                            });
                    } else {
                        $('.no-learning-option-selected').html('Nu ati selectat nici o pagina!')
                        $('.no-learning-option-selected').removeClass('hidden')
                    }
                } else if (selectedOption == 'random-order' || selectedOption == 'ordered-order') {
                    var postData = {
                        learning_type: selectedOption,
                        category_id: categoryId,
                        csrfmiddlewaretoken: token // Include the CSRF token in your data
                    };
                    $.post(backendURL, postData, function (response) {
                        console.log(response)
                        if (response.status === 200){
                            urlToRedirect = redirectURL.replace('0', response.session_id)
                            window.location.href = urlToRedirect
                        }
                    })
                        .fail(function (error) {
                            console.error('Error:', error);
                        });

                } else if (selectedOption == 'return-to-progress'){
                    urlToRedirect = redirectURL.replace('0', sessionAlreadyExists)
                    window.location.href = urlToRedirect

                } else {
                    $('.no-learning-option-selected').html('Nu ati selectat nici o optiune!')
                    $('.no-learning-option-selected').removeClass('hidden')
                }
            })
        });
    }

    // Attach click event handlers to .tabs__item
    $('.tabs__item').on('click', function () {
        $('.tabs__item').removeClass('tabs__item--selected');
        $(this).addClass('tabs__item--selected');
        var itemId = $(this).find('div').data('item-id');
        updateSubCategories(itemId);
    });
    // Attach initial click event handlers to .sub-category
    attachSubCategoryClickHandlers();

    $('.learning-option').on('click', function () {
        var clickedId = $(this).attr('id');
        $('.learning-option').removeClass('learning-option--selected');
        $(this).addClass('learning-option--selected ');
        $('#page-number-container').removeClass('hidden')
        $('.no-learning-option-selected').addClass('hidden')
        if (clickedId == 'page-number-order') {
            $(".page__search--input").on("input", function () {
                const predefinedList = [1, 2, 3, 4, 5, 6, 77, 67, 1001];
                const searchText = $(this).val();
                const filteredResults = predefinedList.filter(item => item.toString().includes(searchText));
                const searchResultsContainer = $(".page__search--results");
                searchResultsContainer.empty();

                if (filteredResults.length > 0 && searchText.length > 0) {
                    searchResultsContainer.removeClass('hidden')
                    filteredResults.forEach(result => {
                        const resultItem = $("<div class='search-result-item'>" + result + "</div>");
                        resultItem.on("click", function () {
                            $(".page__search--input").val(result);
                            searchResultsContainer.hide();
                            $('.no-learning-option-selected').addClass('hidden')
                            if (selectedList.indexOf(result) === -1) {
                                var html = '<div class="chip" data-value=' + result + '>' + result + '<span class="delete-page"><i class="fa-solid fa-xmark"></i></span></div>';
                                $('.selected__pages').append(html);
                                $('.delete-page').on("click", function () {
                                    var parentDataValue = $(this).parent().data('value');
                                    var index = selectedList.indexOf(parentDataValue);
                                    if (index !== -1) {
                                        selectedList.splice(index, 1);
                                    }
                                    $(this).parent().remove()
                                });
                                selectedList.push(result)
                            }
                        });
                        searchResultsContainer.append(resultItem);
                    });
                    searchResultsContainer.show();
                } else {
                    searchResultsContainer.hide();
                }
            })
        } else {
            $('#page-number-container').addClass('hidden')
        }

    });
});