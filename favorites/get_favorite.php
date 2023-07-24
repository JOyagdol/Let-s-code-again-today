<?php
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    //!변수설정
    $getData = $_GET;
    $phone = $getData['phone'];
    $jobid = $getData['jobid'];

    //!db연결
    $conn = new mysqli('localhost', 'root', '1234', 'app');
    if ($conn->connect_error) {
        die('Connection failed: ' . $conn->connect_error);
    }

    //!변수설정2
    $phone = $conn->real_escape_string($phone);
    $jobid = $conn->real_escape_string($jobid);

    //!즐겨찾기 상태 가져오기
    try {
        $stmt = $conn->prepare("SELECT 1 FROM favorites WHERE phone = ? AND jobid = ?");
        $stmt->bind_param("ss", $phone, $jobid);
        $stmt->execute();
        $stmt->store_result();
        //!즐겨찾기된 상태이면 echo "노란별"
        //!즐겨찾기된 상태가 아니면 echo "흰별"
        $isMatch = ($stmt->num_rows > 0);
        echo $isMatch ? '노란별' : '흰별';
    } catch (Exception $e) {
        echo 'Error: ' . $e->getMessage();
    } finally {
        $stmt->close();
        $conn->close();
    }
}
?>
