Robot Tìm Đường
1. Nội dung chi tiết
Cho một bản đồ phẳng xOy (góc phần tư I), trên đó người ta đặt một điểm bắt đầu
S(xs, ys) và một điểm đích đến G(xG,yG). Đồng thời đặt các chướng ngại vật là các hình
đa giác lồi sao cho các đa giác không được đặt chồng lên nhau hay có điểm chung.
Không gian bản đồ được giới hạn trong một khung hình chữ nhật có góc trái dưới trùng
09/2019
- 2 -
với gốc tọa độ, độ dày của khung là 1 đơn vị. Không có điểm nào trong bản đồ được vượt
hay đè lên khung này.
Chọn và cài đặt các thuật toán để tìm kiếm đường đi ngắn nhất từ S đến G sao cho
đường đi không được cắt xuyên qua các đa giác. Đường đi có thể men theo cạnh của đa
giác nhưng không được đè lên cạnh của nó. Biểu diễn đồ họa có thể ở mức đơn giản nhất
để người sử dụng thấy được các đa giác và đường đi.
Mức độ thực hiện được chia theo các mức như sau:
- Mức 1: cài đặt thành công 1 thuật toán để tìm đường đi từ S tới G. Báo
cáo lại thuật toán và quá trình chạy thử. Lưu ý, chạy thử trường hợp không có
đường đi.
- Mức 2: cài đặt ít nhất 3 thuật toán khác nhau (ví dụ tìm kiếm mù, tham
lam, heuristic, …). Báo cáo nhận xét sự khác nhau khi chạy thử 3 thuật toán.
- Mức 3: trên bản đồ sẽ xuất hiện thêm một số điểm khác được gọi là
điểm đón. Xuất phát từ S, sau đó đi đón tất cả các điểm này rồi đến trạng thái
G. Thứ tự các điểm đón không quan trọng. Mục tiêu là tìm ra cách để tổng
đường đi là nhỏ nhất. Báo cáo thuật toán đã áp dụng và quá trình chạy thử.
- Mức 4: các hình đa giác có thể di động được với tốc độ h
tọa độ/s. Cách thức di động có thể ở mức đơn giản nhất là tới lui một khoảng
nhỏ để đảm bảo không đè lên đa giác khác. Chạy ít nhất 1 thuật toán trên đó.
Quay video và đính kèm trực tiếp/link vào báo cáo.
- Mức 5 (chưa làm được): thể hiện mô hình trên không gian 3 chiều (3D).

CÁCH SỬ DỤNG:
-
 Ex: python world.py --input input.txt --search fuzzy
  + --input [-i]: tên tệp input truyền vào
  + --search [-s]: tên các nhiệm vụ thực hiện tương ứng:
      - Dijkstra search: "fuzzy"
      - Greedy search: "greedy"
      - A* search: "astar"
      - Dynamic polygans (mức 4): "moving"
