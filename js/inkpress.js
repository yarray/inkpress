var inkpress = (function() {
    // Due to jquery cannot select g[inkscape:label="Trace"] even when the ':' is escaped
    function getTraceLayer(bg) {
        var result = null;
        $.each($('g', bg), function(_, e) {
            if($(e).attr('inkscape:label') === 'Trace') {
                result = $(e);
            }
        });
        return result;
    }

    function getLoc(pos, shape, panelSize) {
        var scale = Math.max(shape.width / panelSize.width,  shape.height / panelSize.height);
        return {
            centerX: pos.left + shape.viewWidth / 2 - panelSize.width / 2,
            centerY: pos.top + shape.viewHeight / 2 - panelSize.height / 2,
            scale: scale,
            rotate: shape.angle * -180 / Math.PI
        };
    }

    function setStep(step, params) {
        step.attr('data-x', params.centerX);
        step.attr('data-y', params.centerY);
        step.attr('data-scale', params.scale);
        step.attr('data-rotate', params.rotate);
        return step;
    }

    function createStep(id, params) {
        var step = $('<div></div>');
        step.attr('id', id);
        step.addClass('step');
        if (params) {
            setStep(step, params);
        }
        return step;
    }

    function getShape(svgObj) {
        // Here only deal with rotations, since inkscape doesn't use scale in
        // the matrix and skew for a step bbox doesn't make sense
        var width = parseFloat($(svgObj).attr('width'));
        var height = parseFloat($(svgObj).attr('height'));
        var transform = $(svgObj).attr('transform');
        if (transform) {
            var matrix = transform.replace('matrix(', '').replace(')', '').split(',');
            var cos = parseFloat(matrix[0]);
            var sin = parseFloat(matrix[1]);
            var angle = Math.acos(cos);
            var viewHeight = Math.abs(width * sin) + Math.abs(height * cos);
            var viewWidth  = Math.abs(width * cos) + Math.abs(height * sin);
        } else {
            var angle = 0;
            var viewHeight = height;
            var viewWidth = width;
        }

        return {
            width: width,
            height: height,
            viewWidth: viewWidth,
            viewHeight: viewHeight,
            angle: angle
        }
    }

    var init = function(svg_url) {
        $.get(svg_url, function(data) {
            var panelSize = {
                width: 1280.0,
                height: 800.0
            }

            var panel = $('#impress');
            var bg = data.childNodes[1];

            // set the cover page and the background image
            var full = createStep('full').appendTo(panel).append(bg);
            full.height(panelSize.height);
            full.width(panelSize.width);

            // for each bbox in trace ordered by id, create or set steps
            var trace = getTraceLayer(bg);
            var current = full;
            $.each(trace.children().toArray().sort(function(a, b) {
                return parseInt(a.id, 10) - parseInt(b.id, 10)
            }), function(i, bbox) {
                // determine id and params of the corresponding step
                var id = 'step-' + bbox.id;
                var params = getLoc(
                    $(bbox).position(),
                    getShape(bbox),
                    panelSize
                );

                // find existing step, if exist than set params, else create new
                var step = $('#' + id, panel);
                if (step.length > 0) {
                    current = setStep(step, params);
                } else {
                    current = createStep(id, params).insertAfter(current);
                }
            });

            impress().init();
        });
    };

    return {
        init: init
    }
})();
