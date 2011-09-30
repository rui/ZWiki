$def with (keywords="", content=None, quicklinks=True, static_files=None)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Search</title>

    <style>
    #keywords { width : 400px; }
    </style>

    $if static_files:
        $static_files

</head>
<body>


<div id="container">


$if quicklinks:
    <div id="quicklinks">
        <a href="/">Recnet Changes</a>
        <a href="/~index">Index</a>
    </div>

    <hr />


<h2>Search</h2>

<div id="searchbox-not-right">
    <form method="POST" action="/~s" accept-charset="utf-8">
        <input type="text" value="$keywords" name="k" id="keywords" />
        <input type="submit" value="Search" />
    </form>
</div>


$if content:
    <div id="result">
    $content
    </div>


</div>


</body>
</html>