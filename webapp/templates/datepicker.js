/**
 *
 * @authors zx.wang (zx.wang1991@gmail.com)
 * @date    2016-10-09 11:07:00
 * @version $Id$
 */

'use strict';

(function(root, factory) {
  var $ = root.Zepto ? 'zepto' : 'jquery';
  if (typeof define === 'function' && define.amd) {
    define([$], factory);
  } else if (typeof module !== 'undefined' && typeof exports === 'object' && define.cmd) {
    module.exports = factory(require($));
  } else {
    factory(root.jQuery || root.Zepto);
  }

})(this, function($, undefined) {

  if ($.fn.hasOwnProperty('date')) {
    return;
  }

  $.fn.date = function(options, Ycallback, Ncallback) {

    //插件默认选项
    var that = $(this),
      docType = $(this).is('input'),
      datetime = false,
      nowdate = new Date();
    var endyear = nowdate.getFullYear();

    $.fn.date.defaultOptions = {
      //年-开始
      beginyear: 1900,
      //年-结束
      endyear: endyear,
      //月-开始
      beginmonth: 1,
      //月-结束
      endmonth: 12,
      //日-开始
      beginday: 1,
      //日-结束
      endday: 31,
      //小时-开始
      beginhour: 0,
      //小时-结束
      endhour: 23,
      beginminute: 0,
      endminute: 59,
      beginsecond: 0,
      endsecond: 59,
      liH: 40,
      //打开日期是否显示当前日期
      curdate: false,
      //主题（日期；日期+时间）
      theme: 'date',
      //操作模式
      mode: null,
      event: 'click',
      show: true,
      scrollConfig: {
        snap: "li",
        vScrollbar: false
      }
    }

    //用户选项覆盖插件默认选项
    var opts = $.extend(true, {}, $.fn.date.defaultOptions, options);

    var indexY = 1,
      indexM = 1,
      indexD = 1,
      indexH = 1,
      indexI = 1,
      indexS = 0;

    var initY = parseInt((nowdate.getFullYear() - opts.beginyear), 10),
      initM = parseInt((nowdate.getMonth()), 10) + 1,
      initD = parseInt((nowdate.getDate()), 10),
      initH = parseInt(nowdate.getHours()),
      initI = parseInt(nowdate.getMinutes()),
      initS = parseInt(nowdate.getSeconds());

    var yearScroll = null,
      monthScroll = null,
      dayScroll = null,
      hourScroll = null,
      minuteScroll = null,
      secondScroll = null;



    //主题模式
    if (opts.theme === 'datetime') {
      datetime = true;
    }

    //如果不显示取消事件
    if (!opts.show) {
      that.unbind('click');
    } else {
      //绑定点击事件
      that.bind(opts.event, function(event) {
        /* 动态生成空间显示的日期*/
        createUL();
        //初始化iscroll
        initIScroll();
        //显示控件
        extendOptions();
        that.blur();

        //如果是时间主题
        if (datetime) {
          showDateTime();
          refreshTime();
        }

        refreshDate();
        bindButton();
      });
    };

    //刷新日期
    function refreshDate() {
      //iscroll刷新
      yearScroll.refresh();
      monthScroll.refresh();
      dayScroll.refresh();

      //重置日期
      resetInitDate();

      yearScroll.scrollTo(0, initY * opts.liH, 100, true);
      monthScroll.scrollTo(0, initM * opts.liH - opts.liH, 100, true);
      dayScroll.scrollTo(0, initD * opts.liH - opts.liH, 100, true);
    }

    //刷新时间
    function refreshTime() {

      hourScroll.refresh();
      minuteScroll.refresh();
      secondScroll.refresh();

      resetInitTime();

      hourScroll.scrollTo(0, initH * opts.liH, 100, true);
      minuteScroll.scrollTo(0, initI * opts.liH, 100, true);
      secondScroll.scrollTo(0, initS * opts.liH, 100, true);

      //initH = parseInt(nowdate.getHours());

    }

    //重置index
    function resetIndex() {
      indexY = 1;
      indexM = 1;
      indexD = 1;
    }

    //重置日期
    function resetInitDate() {
      //debugger;
      if (opts.curdate) {
        return false;
      } else if (that.val() === '') {
        return false;
      }
      initY = parseInt(that.val().substr(0, 4), 10) - 1900;
      initM = parseInt(that.val().substr(5, 2), 10);
      initD = parseInt(that.val().substr(8, 2), 10);


    }

    function resetInitTime() {
      if (opts.curdate) {
        return false;
      } else if (that.val() === '') {
        return false;
      }

      initH = parseInt(that.val().substr(11, 2), 10);
      initI = parseInt(that.val().substr(14, 2), 10);
      initS = parseInt(that.val().substr(17, 2), 10);

    }


    //创建日期dom
    function createUL() {
      createDateUi();
      $("#yearwrapper ul").html(createYearUl());
      $("#monthwrapper ul").html(createMonthUl());
      $("#daywrapper ul").html(createDayUl());
    }

    function createDateUi() {
      var str = '' +
        '<div id="dateshadow" class="date-shadow"></div>' +
        '<div id="datePage" class="page date-page">' +
        '<section>' +
        '<div id="datetitle" class="date-title"><h1>请选择日期</h1></div>' +
        '<div id="datemark" class="date-mark">' +
        '<a id="markyear" class="mark-year"></a>' +
        '<a id="markmonth" class="mark-month"></a>' +
        '<a id="markday" class="mark-day"></a>' +
        '</div>' +
        '<div id="timemark" class="time-mark">' +
        '<a id="markhour" class="mark-hour"></a>' +
        '<a id="markminute" class="mark-minute"></a>' +
        '<a id="marksecond" class="mark-second"></a>' +
        '</div>' +
        '<div id="datescroll" class="date-scroll">' +
        '<div id="yearwrapper" class="year-wrapper">' +
        '<ul></ul>' +
        '</div>' +
        '<div id="monthwrapper" class="month-wrapper">' +
        '<ul></ul>' +
        '</div>' +
        '<div id="daywrapper" class="day-wrapper">' +
        '<ul></ul>' +
        '</div>' +
        '</div>' +

        '<div id="datescroll_datetime" class="date-scroll-datetime">' +
        '<div id="hourwrapper" class="hour-wrapper">' +
        '<ul></ul>' +
        '</div>' +
        '<div id="minutewrapper" class="minute-wrapper">' +
        '<ul></ul>' +
        '</div>' +
        '<div id="secondwrapper" class="second-wrapper">' +
        '<ul></ul>' +
        '</div>' +
        '</div>' +
        '</section>' +
        '<footer id="dateFooter" class="date-footer">' +
        '<div id="setcancel" class="set-cancel">' +
        '<ul>' +
        '<li id="dateconfirm" class="date-confirm">确定</li>' +
        '<li id="datecancel" class="date-cancel">取消</li>' +
        '</ul>' +
        '</div>' +
        '</footer>' +
        '</div>';
      if (!$('#datePlugin').size()) {
        $('body').append('<div id="datePlugin"></div>');
      }
      $('#datePlugin').html(str);
    }

    //创建年列表
    function createYearUl() {
      var str = '<li>&nbsp;</li>';
      for (var i = opts.beginyear; i <= opts.endyear; i++) {
        str += '<li>' + i + '年</li>';
      }
      return str + '<li>&nbsp;</li>';
    }

    //创建月列表
    function createMonthUl() {
      var str = '<li>&nbsp;</li>';
      for (var i = opts.beginmonth; i <= opts.endmonth; i++) {
        i = i < 10 ? '0' + i : i;
        str += '<li>' + i + '月</li>';
      }

      return str + '<li>&nbsp;</li>';
    }

    //创建日列表
    function createDayUl() {
      //?
      $('#daywrapper ul').html('');
      var str = '<li>&nbsp;</li>';

      for (var i = opts.beginday; i <= opts.endday; i++) {
        i = i < 10 ? '0' + i : i;
        str += '<li>' + i + '日</li>';
      }

      return str + '<li>&nbsp;</li>';
    }

    //创建时列表(记得修改成24小时制)
    function createHourUl() {
      var str = '<li>&nbsp;</li>';
      for (var i = opts.beginhour; i <= opts.endhour; i++) {
        i = i < 10 ? '0' + i : i;
        str += '<li>' + i + '时</li>';
      }

      return str + '<li>&nbsp;</li>';
    }

    //创建分列表
    function createMinuteUl() {
      var str = '<li>&nbsp;</li>';
      for (var i = opts.beginminute; i <= opts.endminute; i++) {
        i = i < 10 ? '0' + i : i;
        str += '<li>' + i + '分</li>';
      }

      return str + '<li>&nbsp;</li>';
    }

    //创建秒列表
    function createSecondUl() {
      var str = '<li>&nbsp;</li>';
      for (var i = opts.beginsecond; i <= opts.endsecond; i++) {
        i = i < 10 ? '0' + i : i;
        str += '<li>' + i + '秒</li>';
      }
      return str + '<li>&nbsp;</li>';
    }

    //添加时间样式
    function addTimeStyle() {
      var style = {
        'position': 'absolute',
        'bottom': '200px'
      };

      $('#datePage').css({
        'height': '380px',
        'top': '60px'
      });
      $('#yearwrapper').css({
        'position': 'absolute',
        'bottom': '200px'
      });
      $('#monthwrapper').css({
        'position': 'absolute',
        'bottom': '200px'
      });
      $('#daywrapper').css({
        'position': 'absolute',
        'bottom': '200px'
      });
    }

    //日期滑动
    function initIScroll() {
      var strY = $('#yearwrapper').find('li').eq(indexY).html();
      strY = strY.length > 0 ? strY.substr(0, strY.length - 1) : '';
      var strM = $('#monthwrapper').find('li').eq(indexM).html();
      strM = strM.length > 0 ? strM.substr(0, strM.length - 1) : '';

      yearScroll = new iScroll('yearwrapper', $.extend(true, {}, opts.scrollConfig, {
        onScrollEnd: function() {
          indexY = Math.round((this.y / opts.liH) * (-1)) + 1;
          strY = $('#yearwrapper').find('li').eq(indexY).html();
          strY = strY.length > 0 ? strY.substr(0, strY.length - 1) : '';
          opts.endday = checkdays(strY, strM);

          $('#daywrapper').find('ul').html(createDayUl());
          dayScroll.refresh();
        }
      }));
      monthScroll = new iScroll('monthwrapper', $.extend(true, {}, opts.scrollConfig, {
        onScrollEnd: function() {
          //debugger;
          indexM = Math.round((this.y / opts.liH) * (-1)) + 1;
          //console.log(indexM);
          strM = $('#monthwrapper').find('li').eq(indexM).html();
          strM = strM.length > 0 ? strM.substr(0, strM.length - 1) : '';

          opts.endday = checkdays(strY, strM);
          $('#daywrapper').find('ul').html(createDayUl());
          dayScroll.refresh();
        }
      }));
      dayScroll = new iScroll('daywrapper', $.extend(true, {}, opts.scrollConfig, {
        onScrollEnd: function() {
          indexD = Math.round((this.y / opts.liH) * (-1)) + 1;
        }
      }));


    }

    //日期+时间滑动
    function initIScrollDateTime() {

      hourScroll = new iScroll('hourwrapper', $.extend(true, {}, opts.scrollConfig, {
        onScrollEnd: function() {
          indexH = Math.round((this.y / opts.liH) * (-1)) + 1;
          hourScroll.refresh();
        }
      }));
      minuteScroll = new iScroll('minutewrapper', $.extend(true, {}, opts.scrollConfig, {
        onScrollEnd: function() {
          indexI = Math.round((this.y / opts.liH) * (-1)) + 1;
          hourScroll.refresh();
        }
      }));
      secondScroll = new iScroll('secondwrapper', $.extend(true, {}, opts.scrollConfig, {
        onScrollEnd: function() {
          indexS = Math.round((this.y / opts.liH) * (-1)) + 1;
          hourScroll.refresh();
        }
      }));

    }

    //显示时分秒时间
    function showDateTime() {
      initIScrollDateTime();
      addTimeStyle();
      $("#datescroll_datetime").show();
      $("#hourwrapper ul").html(createHourUl());
      $("#minutewrapper ul").html(createMinuteUl());
      $("#secondwrapper ul").html(createSecondUl());
    }

    //检查当前天数
    function checkdays(year, month) {
      //当前年
      var newyear = year;
      //下一个月
      var newmonth = month++;
      if (month > 12) {
        newmonth -= 12;
        newyear++;
      }

      //取当年当月第一天
      var newdate = new Date(newyear, newmonth, 1);

      //返回当月最后一天的日期
      return (new Date(newdate.getTime() - 1000 * 60 * 60 * 24)).getDate();
    }



    //显示组件
    function extendOptions() {
      $('#datePage').show();
      $('#dateshadow').show();
    }

    //绑定事件
    function bindButton() {
      //重置Index
      resetIndex();

      //点击确定
      $('#dateconfirm').on('click', function() {
        //debugger;
        var yearstr = $('#yearwrapper').find('li').eq(indexY).html();
        var monthstr = $('#monthwrapper').find('li').eq(indexM).html();
        var daystr = $('#daywrapper').find('li').eq(indexD).html();
        yearstr = (yearstr.length > 0) ? yearstr.substr(0, yearstr.length - 1) : '';
        monthstr = (monthstr.length > 0) ? monthstr.substr(0, monthstr.length - 1) : '';
        daystr = (daystr.length > 0) ? daystr.substr(0, daystr.length - 1) : '';
        var datestr = yearstr + '-' + monthstr + '-' + daystr;

        //如果显示时分秒
        if (datetime) {

          var hourstr = $('#hourwrapper').find('li').eq(indexH).html();
          hourstr = (hourstr.length > 0) ? hourstr.substr(0, hourstr.length - 1) : '';
          //var hour = parseInt(hourstr, 10);

          var minutestr = $("#minutewrapper").find('li').eq(indexI).html();
          minutestr = (minutestr.length > 0) ? minutestr.substr(0, minutestr.length - 1) : '';

          var secondstr = $('#secondwrapper').find('li').eq(indexS).html();
          secondstr = (secondstr.length > 0) ? secondstr.substr(0, secondstr.length - 1) : '';

          datestr += ' ' + hourstr + ':' + minutestr + ':' + secondstr;

        }

        if (docType) {
          that.val(datestr);
        } else {
          that.html(datestr);
        }

        $('#datePlugin').html('');
        //成功回调
        Ycallback && Ycallback(datestr);
      });

      $('#datecancel').on('click', function() {
        $('#datePlugin').html('');
        //取消回调
        Ncallback && Ncallback(false);
      });
    }
  }
});
