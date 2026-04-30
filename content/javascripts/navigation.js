(function () {
  function scrollContainerToElement(container, element, topOffset) {
    if (!container || !element || !element.offsetHeight) return;

    var elementRect = element.getBoundingClientRect();
    var containerRect = container.getBoundingClientRect();
    var top = container.scrollTop + elementRect.top - containerRect.top - (topOffset || 0);

    container.scrollTo({ top: Math.max(0, top) });
  }

  function isScrollable(element) {
    if (!element || element === document.body) return false;
    return element.scrollHeight > element.clientHeight;
  }

  // With navigation.tabs, Material applies position:sticky;top:0 to the active
  // section header (.md-nav--lifted > ... > .md-nav__link). This header sits at
  // the top of the scrollwrap and covers the first visible nav item. Return its
  // height so the scroll target can be offset past it.
  function getStickyTopOffset(sidebar) {
    var el = sidebar.querySelector(
      '.md-nav--lifted > .md-nav__list > .md-nav__item--active > .md-nav__link'
    );
    // Add extra pixels to clear the box-shadow (.4rem blur + .4rem spread)
    // that bleeds below the header's border box.
    return el ? el.offsetHeight + 8 : 0;
  }

  function currentPageLink(sidebar) {
    var links = sidebar.querySelectorAll('.md-nav__link[href]');
    var currentPath = new URL(window.location.href).pathname.replace(/\/$/, '');

    for (var index = 0; index < links.length; index += 1) {
      var link = links[index];
      var linkPath = new URL(link.href, window.location.href).pathname.replace(/\/$/, '');

      if (linkPath !== currentPath) continue;

      if (link.offsetHeight) return link;

      // At narrow widths (<60em) Material hides the <a> and shows a <label for="__toc">
      // sibling instead. Find the first visible direct-child nav link in the same item.
      var item = link.closest('.md-nav__item');
      if (item) {
        var candidates = item.querySelectorAll(':scope > .md-nav__link');
        for (var j = 0; j < candidates.length; j += 1) {
          if (candidates[j].offsetHeight) return candidates[j];
        }
      }

      return link;
    }

    return null;
  }

  function scrollActivePrimaryNavToTop() {
    var sidebar = document.querySelector('.md-sidebar--primary');
    if (!sidebar) return;

    var activeLink = currentPageLink(sidebar);
    if (!activeLink || !activeLink.offsetHeight) return;

    var topOffset = getStickyTopOffset(sidebar);

    var container = activeLink.parentElement;
    while (container && container !== sidebar.parentElement) {
      if (isScrollable(container)) {
        scrollContainerToElement(container, activeLink, topOffset);
      }
      container = container.parentElement;
    }
  }

  function fixExceptionsTableWrappers() {
    var tables = document.querySelectorAll('table[data-ssl-table="exceptions"]');
    for (var i = 0; i < tables.length; i += 1) {
      var table = tables[i];
      // Material's .md-typeset table:not([class]) rule sets display:inline-block
      // with higher specificity than the wrapper rule, so override it directly.
      table.style.display = 'table';
      table.style.width = '100%';
      var wrapper = table.parentElement;
      if (wrapper && wrapper.classList.contains('md-typeset__table')) {
        wrapper.style.display = 'block';
      }
    }
  }

  function scheduleScroll() {
    [0, 150, 350, 650].forEach(function (delay) {
      window.setTimeout(function () {
        window.requestAnimationFrame(function () {
          scrollActivePrimaryNavToTop();
          fixExceptionsTableWrappers();
        });
      }, delay);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scheduleScroll);
  } else {
    scheduleScroll();
  }

  if (window.document$) {
    window.document$.subscribe(scheduleScroll);
  }

  document.addEventListener('change', function (event) {
    if (event.target && event.target.matches('.md-nav__toggle, [data-md-toggle="drawer"]')) {
      scheduleScroll();
    }
  });

  document.addEventListener('click', function (event) {
    if (event.target && event.target.closest('label[for^="__nav_"]')) {
      scheduleScroll();
    }
  });
})();
