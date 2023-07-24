<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    //!변수설정
    $postData = json_decode(file_get_contents('php://input'), true);
    $name = $postData['name'];
    $address = $postData['address'];
    $phone = $postData['phone'];
    $career1 = $postData['career1'];
    $career2 = $postData['career2'];
    $hope1 = $postData['hope1'];
    $hope2 = $postData['hope2'];

    // !db연결
    $conn = new mysqli('localhost', 'root', '1234', 'app');
    if ($conn->connect_error) {
        die('Connection failed: ' . $conn->connect_error);
    }

    //!변수설정2
    $name = $conn->real_escape_string($name);
    $address = $conn->real_escape_string($address);
    $phone = $conn->real_escape_string($phone);
    $career1 = $conn->real_escape_string($career1);
    $career2 = $conn->real_escape_string($career2);
    $hope1 = $conn->real_escape_string($hope1);
    $hope2 = $conn->real_escape_string($hope2);

    //!변경된 정보로 update
    try {
        $checkQuery = "SELECT phone FROM user WHERE phone = '$phone'";
        $checkResult = $conn->query($checkQuery);

        if ($checkResult->num_rows > 0) {
            $updateQuery = "UPDATE user SET name = '$name', address = '$address', career1 = '$career1', career2 = '$career2', hope1 = '$hope1', hope2 = '$hope2' WHERE phone = '$phone'";
            if ($conn->query($updateQuery) === true) {
                echo "Form data updated successfully in the database!";
            } else {
                throw new Exception("Error: " . $updateQuery . "<br>" . $conn->error);
            }
        }
    } catch (Exception $e) {
        echo $e->getMessage();
    }
    $conn->close();
}
?>
