<?php
    //!기능 미적용
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    //!변수설정
    $getData = $_GET;
    $jobid = $getData['jobid'];

    //!db연결
    $conn = new mysqli('localhost', 'root', '1234', 'app');
    if ($conn->connect_error) {
        die('Connection failed: ' . $conn->connect_error);
    }
    $conn->set_charset('utf8');

    //!변수설정2
    $phone = $conn->real_escape_string($phone);

    //!jobid의 oranNm,recrtTitle,workPlcNm,emplymShp 검색
    try {
        $stmt = $conn->prepare("SELECT oranNm,recrtTitle,workPlcNm,emplymShp FROM favorites WHERE jobid = ?");
        $stmt->bind_param("s", $jobid);
        $stmt->execute();
        $stmt->store_result();
        $stmt->bind_result($oranNm,$recrtTitle,$workPlcNm,$emplymShp);
        $resultArray = array();
        if($emplymShp =='CM0101'){
          $emplymShp='정규직';
        }elseif($emplymShp =='CM0102'){
          $emplymShp='계약직';
        }elseif($emplymShp =='CM0103'){
          $emplymShp='시간제일자리';
        }elseif($emplymShp =='CM0104'){
          $emplymShp='일당직';
        }elseif($emplymShp =='CM0105'){
          $emplymShp='기타';
        }
        $data = array(
          'oranNm' => $oranNm,
          'recrtTitle' => $recrtTitle,
          'workPlcNm' => $workPlcNm,
          'emplymShp' => $emplymShp,
        );
        $resultArray[] = $data;
        $stmt->close();
        $conn->close();
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($resultArray, JSON_UNESCAPED_UNICODE);
    } catch (Exception $e) {
        echo 'Error: ' . $e->getMessage();
    }
}
?>
