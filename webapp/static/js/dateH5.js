(function ($) {
    $.fn.date = function (options, Ycallback, Ncallback) {
        var that = $(this);
        var docType = $(this).is('input');
        var nowdate = new Date();
        var indexY = 1,
            indexM = 1;
        var initY = parseInt(nowdate.getFullYear());
        var initM = parseInt(nowdate.getMonth() + "") + 1;
        var yearScroll = null,
            monthScroll = null;
        var startYear = nowdate.getFullYear();
        $.fn.date.defaultOptions = {
            beginyear: startYear,
            endyear: startYear + 100,
            beginmonth: 1,
            endmonth: 12,
            curdate: true,
            theme: "date",
            mode: null,
            event: "click",
            show: true
        }
        const opts = $.extend(true, {}, $.fn.date.defaultOptions, options);
        if (!opts.show) {
            that.unbind('click');
        } else {
            that.bind(opts.event, function () {
                createUL();
                init_iScroll();
                extendOptions();
                that.blur();
                refreshDate();
                bindButton();
            })
        }

        function refreshDate() {
            yearScroll.refresh();
            monthScroll.refresh();

            resetInitDate();
            yearScroll.scrollTo(0, 40, 100, true);
            monthScroll.scrollTo(0, 40, 100, true);
        }

        function resetIndex() {
            indexY = 1;
            indexM = 1;
        }

        function resetInitDate() {
            if (opts.curdate) {
                return false;
            } else if (that.val() === "") {
                return false;
            }
            initY = parseInt(that.val().substr(0, 4));
            initM = parseInt(that.val().substr(5, 2));
        }

        function bindButton() {
            resetIndex();
            $("#dateconfirm").unbind('click').click(function () {
                var datestr = $("#yearwrapper ul li:eq(" + indexY + ")").html().substr(0, $("#yearwrapper ul li:eq(" + indexY + ")").html().length) + "-" +
                    $("#monthwrapper ul li:eq(" + indexM + ")").html().substr(0, $("#monthwrapper ul li:eq(" + indexM + ")").html().length);

                if (Ycallback === undefined) {
                    if (docType) {
                        that.val(datestr);
                    } else {
                        that.html(datestr);
                    }
                } else {
                    Ycallback(datestr);
                }
                $("#datePage").hide();
                $("#dateshadow").hide();
            });
            $("#datecancel").click(function () {
                $("#datePage").hide();
                $("#dateshadow").hide();
                Ncallback(false);
            });
        }

        function extendOptions() {
            $("#datePage").show();
            $("#dateshadow").show();
        }

        function init_iScroll() {
            var strY = $("#yearwrapper ul li:eq(" + indexY + ")").html().substr(0, $("#yearwrapper ul li:eq(" + indexY + ")").html().length - 1);
            var strM = $("#monthwrapper ul li:eq(" + indexM + ")").html().substr(0, $("#monthwrapper ul li:eq(" + indexM + ")").html().length - 1);
            yearScroll = new iScroll("yearwrapper", {
                snap: "li",
                vScrollbar: false,
                onScrollEnd: function () {
                    indexY = Math.round((this.y / 40) * (-1)) + 1;
                    strY = $("#yearwrapper ul li:eq(" + indexY + ")").html().substr(0, $("#yearwrapper ul li:eq(" + indexY + ")").html().length - 1);
                }
            });
            monthScroll = new iScroll("monthwrapper", {
                snap: "li",
                vScrollbar: false,
                onScrollEnd: function () {
                    indexM = Math.round((this.y / 40) * (-1)) + 1;
                    strM = $("#monthwrapper ul li:eq(" + indexM + ")").html().substr(0, $("#monthwrapper ul li:eq(" + indexM + ")").html().length - 1);
                }
            });
        }

        function createUL() {
            CreateDateUI();
            $("#yearwrapper").find('ul').html(createYEAR_UL());
            $("#monthwrapper").find('ul').html(createMONTH_UL());
        }

        function CreateDateUI() {
            const str = '' +
                '<div id="dateshadow"></div>' +
                '<div id="datePage" class="page">' +
                '<section>' +
                '<div id="datetitle">' +
                    '<h5 id="datetitleheader">The expiration date of the medicine</h5>' +
                '</div>' +
                '<div id="datemark">' +
                    '<a id="markyear"></a>' +
                    '<a id="markmonth"></a>' +
                '</div>' +

                '<div id="datescroll">' +
                    '<div id="yearwrapper">' +
                        '<ul></ul>' +
                    '</div>' +
                        '<div id="monthwrapper">' +
                            '<ul></ul>' +
                        '</div>' +
                    '</div>' +
                    '</section>' +
                    '<footer id="dateFooter">' +
                        '<div id="setcancle">' +
                            '<ul>' +
                                '<li id="dateconfirm">Confirm</li>' +
                                '<li id="datecancel">Cancel</li>' +
                            '</ul>' +
                        '</div>' +
                    '</footer>' +
                '</div>'
            $("#datePlugin").html(str);
        }

        function createYEAR_UL() {
            let str = "<li>&nbsp;</li>";
            for (let i = opts.beginyear; i <= opts.endyear; i++) {
                str += '<li>' + i + '</li>'
            }
            return str + "<li>&nbsp;</li>";
        }

        function createMONTH_UL() {
            let str = "<li>&nbsp;</li>";
            for (let i = opts.beginmonth; i <= opts.endmonth; i++) {
                if (i < 10) {
                    i = "0" + i
                }
                str += '<li>' + i + '</li>'
            }
            return str + "<li>&nbsp;</li>";
        }
    }
})(typeof (Zepto) != 'undefined' ? Zepto : jQuery);
