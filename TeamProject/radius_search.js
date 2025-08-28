// radius_search.js 파일 내용

// 카카오 지도 초기화
var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 서울 시청을 초기 중심으로 설정
        level: 3 // 지도의 확대 레벨
    };

// 지도를 생성
var map = new kakao.maps.Map(mapContainer, mapOption); 

// 주소-좌표 변환 객체를 생성
var geocoder = new kakao.maps.services.Geocoder();

// 검색 버튼에 클릭 이벤트 리스너를 추가
document.querySelector('.input-group button').addEventListener('click', function() {
    var address = document.querySelector('.input-group input').value;

    // 주소로 좌표를 검색
    geocoder.addressSearch(address, function(result, status) {
        // 정상적으로 검색이 완료됐으면
        if (status === kakao.maps.services.Status.OK) {
            var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

            // 지도 중심을 검색된 위치로 이동
            map.setCenter(coords);
            
            // 기존 마커 및 반경 원 삭제
            if (marker) {
                marker.setMap(null);
            }
            if (circle) {
                circle.setMap(null);
            }

            // 결과값으로 받은 위치를 마커로 표시
            marker = new kakao.maps.Marker({
                map: map,
                position: coords
            });

            // 반경(예: 3km)을 나타내는 원을 지도에 그립니다.
            circle = new kakao.maps.Circle({
                center : coords,  // 원의 중심좌표
                radius: 3000, // 미터 단위 원의 반지름
                strokeWeight: 2, // 선의 두께 
                strokeColor: '#FF00FF', // 선의 색깔
                strokeOpacity: 0.8, // 선의 불투명도 
                strokeStyle: 'solid', // 선의 스타일
                fillColor: '#FF00FF', // 채우기 색깔
                fillOpacity: 0.3  // 채우기 불투명도 
            }); 

            circle.setMap(map);
        } else {
            alert('주소 검색 결과가 없습니다.');
        }
    });
});