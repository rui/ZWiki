$def with (title, err_info=None, static_files=None)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Editing $title</title>

    $if static_files:
        $static_files

</head>
<body>


<h2>Rename: $title</h2>

<div id="rename">
    <form method="POST" accept-charset="utf-8">
        New name: <input type="text" value="$title" name="new_path" /><br />
        <div id="toolbox">
            <input type="submit" value="Rename" />
        </div>
    </form>
</div>


</body>
</html>