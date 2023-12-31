import numpy as np

#อ่านไฟส์ data.txt
def read_file(filename):
    matrix = np.loadtxt(filename, dtype=int)
    return matrix

#นำไฟส์มาทำ 10% cross validation โดยแบ่งข้อมูล 90% ออกมาเป็น train_data และ ข้อมูลอีก 10% ออกมาเป็น test_data เป็น 10 ช่วง
def split_data_into_segments(data, num_segments):
    segment_size = len(data) // num_segments

    test_data = []
    train_data = []

    for i in range(num_segments):
        start = i * segment_size
        end = (i + 1) * segment_size

        test = data[start:end]
        train = np.concatenate([data[:start], data[end:]])

        test_data.append(test)
        train_data.append(train)

    return test_data, train_data

#นำข้อมูล data.txt มาหา min และ max โดยการใช้ flatten เป็น array 1 มิติ
def getmaxmin(data):
    count = np.array(data).flatten() 
    max = np.max(count)
    min = np.min(count)
    return max, min

#นำข้อมูล data.txt มาหาแปลงให้อยู่ในช่วง 0-1
def normalize(data, mindata, maxdata):
    normalized_data = (data - mindata) / (maxdata - mindata)
    return normalized_data

# แปลงข้อมูล data เป็น normalize
def normalize_data(data):
    min,max=getmaxmin(data)
    normalize_data=normalize(data,min,max)
        
    #แยกข้อมูล input และ output ออกมา
    input = normalize_data[:, :8]
    output = normalize_data[:, 8]   
    return input , output

#นำข้อมูล data.txt อยู่ในช่วงข้อมูลอยู่ในช่วง 0-1 มาแปลงกลับให้อยู่ในฐานข้อมูลเดิม
def inverse_normalize(normalizedata,data): 
    min,max=getmaxmin(data)  
    inverse_normalize = (normalizedata*(max-min))+min
    return inverse_normalize
   
# ฟังก์ชันคำนวณ sigmoid
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# ฟังก์ชันคำนวณ sigmoid derivative
def sigmoid_derivative(x):
    return x * (1 - x)
    
#อัพเดทค่าออกจาก hidden note และ output note
def forward_propagation(input_data):
    hidden = sigmoid(np.dot(w_input_to_hidden, input_data.T) + b_hidden)
    output = sigmoid(np.dot(w_hidden_to_output, hidden) + b_output)

    return hidden, output

#อัพเดทค่า weight ระหว่าง input เข้า hidden note และ bias เข้า hidden note
def update_input_hidden_layer_weights(input_data, hidden_gradient, learning_rate, momentum_rate):
    global w_input_to_hidden, b_hidden, v_w_input_hidden, v_b_hidden
    v_w_input_hidden = (momentum_rate * v_w_input_hidden) + (learning_rate * np.dot(hidden_gradient, input_data) / len(input_data))
    w_input_to_hidden += v_w_input_hidden

    v_b_hidden = (momentum_rate * v_b_hidden) + (learning_rate * np.mean(hidden_gradient, axis=1, keepdims=True))
    b_hidden += v_b_hidden
    
#อัพเดทค่า weight ระหว่าง hidden note เข้า output note และ bias เข้า output note
def update_hidden_output_layer_weights(hidden, output_gradient, learning_rate, momentum_rate):
    global w_hidden_to_output, b_output, v_w_hidden_output, v_b_output
    v_w_hidden_output = (momentum_rate * v_w_hidden_output) + (learning_rate * np.dot(output_gradient, hidden.T) / len(hidden))
    w_hidden_to_output += v_w_hidden_output

    v_b_output = (momentum_rate * v_b_output) + (learning_rate * np.mean(output_gradient, axis=1, keepdims=True))
    b_output += v_b_output

#นำชุดข้อมูลมาเทรน    
def train_custom_neural_network(inputdata, outputdata,Target_Epochs,Mean_Squared_Error, learning_rate, momentum_rate):
    
    for epochs in range(Target_Epochs):
        
        hidden, output = forward_propagation(inputdata) 

        output_error = outputdata - output
        output_gradient = output_error * sigmoid_derivative(output)
        update_hidden_output_layer_weights(hidden, output_gradient, learning_rate, momentum_rate)
    
        hidden_error = np.dot(w_hidden_to_output.T, output_gradient)
        hidden_gradient = hidden_error * sigmoid_derivative(hidden)
        update_input_hidden_layer_weights(inputdata, hidden_gradient, learning_rate, momentum_rate) 
        
        error = np.mean(output_error**2)
        #ปรับค่า epoch ที่ต้องการให้แสดงใน terminal
        #if epochs % 100 == 0 : # epochs % 10000 == 0
            #print(f"Epoch loop: {epochs+100}, Error: {error}")#epochs+10000
                   
        if error <= Mean_Squared_Error:
            break
    
#ค่าคำทำนายจากโปรแกรมกับค่าที่เกิดขึ้นจริงมาหาความคลาดเคลื่อน
def calculate_accuracy(actual, predicted):
    # คำนวณความคลาดเคลื่อนร้อยละ
    errors = np.abs((actual - predicted) / actual) * 100

    # คำนวณค่า Accuracy โดยหาค่าเฉลี่ยของความถูกต้อง
    Accuracy = 100 - np.mean(errors)
    
    return Accuracy

################################################# Main ####################################################################     
#นำไฟส์ data เข้า
file = "dataval.txt"
data = read_file(file)
#print(data.shape)
#print(data)

# กำหนดขนาด Input layer, Hidden layer , Output layer จากชุดข้อมูลที่กำหนดให้
input_size = 8
hidden_size = 4 # สามารถกำหนดเองได้
output_size = 1


# ปรับ learning_rates และ momentum_rates ตามที่ต้องการ
learning_rates = [0.1,0.5]
momentum_rates = [0.01,0.2]

K_segments = 10

print(f"Hidden node = {hidden_size}")

for i in range(K_segments):
    
    #initialize weight แตกต่างกัน โดย สร้างตัวแปร array สุ่มค่า weight และ bias ปัจจุบัน รวมถึง สร้างตัวแปร array สุ่มค่า weight และ bias ก่อนหน้า
    #weight ระหว่าง input note เข้า hidden note
    w_input_to_hidden = np.random.randn(hidden_size, input_size)
    v_w_input_hidden = np.random.randn(hidden_size, input_size)

    #weight ระหว่าง hidden note เข้า output note
    w_hidden_to_output = np.random.randn(output_size, hidden_size)
    v_w_hidden_output = np.random.randn(output_size, hidden_size)
        
    #bias เข้า hidden note 
    b_hidden = np.random.randn(hidden_size, 1)
    v_b_hidden = np.random.randn(hidden_size, 1)
        
    #bias เข้า  note 
    b_output = np.random.randn(output_size, 1)
    v_b_output = np.random.randn(output_size, 1)

    for lr in learning_rates:
        for momentum in momentum_rates:
            
            test_data, train_data = split_data_into_segments(data, K_segments)
            
            print(f"segment ={i+1} Training with learning rate = {lr} and momentum = {momentum} ")
            
            #แปลงข้อมูล train ในอยู่ในช่วง 0-1 โดยการใช้ normalize
            inputtrain_data,outputrain_data = normalize_data(train_data[i])
            
            #นำข้อมูล train มาฝึกโดยสามารถกำหนด จำนวน epoch และ ค่าคลาดเคลื่อนเฉลี่ย MSE ที่ต้องการได้ 
            train_custom_neural_network(inputtrain_data,outputrain_data, 100, 0.0001, lr, momentum)
            
            #แปลงข้อมูล test ในอยู่ในช่วง 0-1 โดยการใช้ normalize    
            inputtest_data,outputtest_data = normalize_data(test_data[i])
            
            #นำข้อมูล test เข้าไปหาค่า Predict output จากการเทรน
            x,Aura=forward_propagation(inputtest_data)
            
            #แปลงข้อมูลจาก normalize เป็นฐานข้อมูลเดิม
            Forture=inverse_normalize(Aura,test_data[i])
            
            #นำข้อมูล Predict output จาก Forture มาเก็บไว้ในตัวแปรใหม่
            Predict = [item for sublist in Forture for item in sublist]
            #นำข้อมูล Actual output จาก test มาเก็บไว้ในตัวแปรใหม่
            Actual = test_data[i][:, 8]
            
            #หาค่าความแม่นยำ
            Accuracy = calculate_accuracy(Actual,Predict)
            
            ########################## แสดงผล
            print("Actual Output    Predict Output          error ")
            for j in range(len(Actual)):
                print(f"     {Actual[j]:<8} | {Predict[j]:<16}   | {abs(Actual[j]-Predict[j])}")
                
            print(f"************Accuracy = {Accuracy} % **************")
