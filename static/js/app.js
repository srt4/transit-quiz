var elementsToRotate= [];

$(document).ready(function() {
    $('.destinations').each(function() {
        elementsToRotate.push($(this));
    });

    $('.route-number-list').click(function(e) {
        rotateChildren($(this));
        e.preventDefault();
        e.stopPropagation();
        console.log($(this).parent().parent().data('correct-route-id'));
        console.log($(this).children(":visible").text().trim());
        if ($(this).parent().parent().data('correct-route-id') ==
              $(this).children(":visible").text().trim()) {
            $(this).css('color', 'green');
            $(this).off();
        }
        return false;
    });

    intervals.push(window.setInterval(function() {
        $.each(elementsToRotate, function(key, value) {
            rotateChildren(value);
        });
    }, 2000));
});

var rotateChildren = function($parentElement) {
    circularFindNextElement($parentElement, function($currentElement, $nextElement) {
        $nextElement.show();
        $currentElement.hide();
    });
};

/**
 *
 * @param $parentElement The element containing the children to rotate
 * @param cb Function accepts parameters ($currentElement, $nextElement)
 */
var circularFindNextElement = function($parentElement, cb) {
    if (!$parentElement.children()) {
        throw new Exception();
    }

    var $visibleElement = $parentElement.children(':visible');

    if ($visibleElement.length > 1 || !$visibleElement.length) {
        console.log("Found " + $visibleElement.length + " visible elements, hiding all and using first child");
        $parentElement.children().hide();
        $nextElement = $parentElement.children().first();
    }
    else {
        var $nextElement = $visibleElement.next();
    }

    if (!$nextElement.length) {
        $nextElement = $parentElement.children().first();
    }

    cb($visibleElement, $nextElement);
}
