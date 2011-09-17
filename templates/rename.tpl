$def with (title)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Editing $title</title>
</head>
<body>

<h2>Rename: $title</h2>

<div id="form">
    <form method="POST" accept-charset="utf-8">
        New name: <input type="text" value="$title" name="new_path" /><br />
        <input type="submit" value="Rename" />
    </form>
</div>

</body>
</html>