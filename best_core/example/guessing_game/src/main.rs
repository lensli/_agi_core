use std::io;
fn main() {
    println!("猜数字游戏！");
    println!("输入猜测的数字：");
    let mut guess = String::new();
    // mut 输的guess 变为可变变量  
    //String 的new 关联函数 会返回一个字符串 实例
    io::stdin()
        .read_line(&mut guess)
        .expect("系统读取数字失败");
    println!("你猜的是：{guess}");
    println!("你猜的是：{}", &mut guess);
    
    let mut x = 10;
    let y = &mut x;
    *y = *y*100;
    println!("y={},",*y);
    println!("y_shm_id ={:p},",y);
    println!("x={}",x);
}
// mut         = "这个变量可以变"（声明）
// &mut        = "这个变量的引用可以用来修改它"（操作）
// &mut	取引用	创建一个指向变量的引用
// *	解引用	打开引用，访问它所指向的值

// // &mut 包含了两层含义：
// //   &   → "我给你个引用"
// //   mut → "这个引用可以修改原变量"
// let mut x = 5;        // 栈上分配内存，x 可以修改

// let y = &mut x;       // 创建一个引用，指向 x 的地址
// *y = 10;
// 内存：
// ┌─────────┐
// │ x = 10  │  ← mut 让这里的值可以改变
// └─────────┘
//     ↑
//     │ &mut x（可变引用指向这里）
//     │
//     y              // 通过这个引用，间接修改 x
