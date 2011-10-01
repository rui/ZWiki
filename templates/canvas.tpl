$def with (title, content, static_files=None, toolbox=True, quicklinks=True)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>$title</title>

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

    <div id="searchbox">
        <form method="POST" action="/~s" accept-charset="utf-8">
            <input type="text" name="k" class="auto-increase-width-size" />
            <input type="submit" value="Search" />
        </form>
    </div>


<div id="title">$title</div>

<div id="content">$content</div>


$if toolbox:
    <div id="toolbox">
        <a href="/$title?action=delete">Delete</a>
        <a href="/$title?action=rename">Rename</a>
        <a href="/$title?action=edit">Edit</a>
    </div>


</div>


</body>
</html>
