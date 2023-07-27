<?php
    //!즐겨찾기 추가와 기능 통합되어 미사용
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    //!변수설정
    $postData = json_decode(file_get_contents('php://input'), true);
    $phone = $postData['phone'];
    $jobid = $postData['jobid'];
    
    //! db연결
    $conn = new mysqli('localhost', 'root', '1234', 'app');
    if ($conn->connect_error) {
        die('Connection failed: ' . $conn->connect_error);
    }

    //!변수설정2
    $phone = $conn->real_escape_string($phone);
    $jobid = $conn->real_escape_string($jobid);

    //!즐겨찾기 제거
    try {
        $stmt = $conn->prepare("DELETE FROM favorites WHERE phone = ? AND jobid = ?");
        $stmt->bind_param("ss", $phone, $jobid);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            echo "Data deleted successfully!";
        } else {
            echo "No matching data found.";
        }
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage();
    } finally {
        $stmt->close();
        $conn->close();
    }
}
?>
