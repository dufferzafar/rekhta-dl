# Rekhta Downloader

## EBoooks

* Fields of interest in the code

```js
var bookid = "";
var bookslug = "";
var pages = [];
var pageIds = [];
var currentPageIdx = 0;
var totalPageCount = 0;
var bookId = "80279b67-ba0e-4a12-8fb5-dcab20187614";

function LoadEbookPage() {
    $.getJSON(
        'https://ebooksapi.rekhta.org/api_getebookpagebyid/?atky=pns&pgi=' + pageIds[currentPageIdx],
        function (data, status) {}
    );
}

function renderEbookPage(data) {

    var s = 50;
    var m = 50;

    Sub[i].X1 * (s + 16), Sub[i].Y1 * (s + 16)  , s, s
    Sub[i].X2 * m       , Sub[i].Y2 * m         , m, m

    $('<img />').attr('src',
        'https://ebooksapi.rekhta.org/images/80279b67-ba0e-4a12-8fb5-dcab20187614/' + pages[currentPageIdx + i + 1 + '']
    );
}
```

* Page images come as a jigsaw puzzle
    * Watermark is not present on the images
        * But added via JS code
        * Won't be an issue

