// // // let a = 0;
// // // let b = false;

// // // console.log(a === b);



// // let a = [1, 2, 3];
// // let b = {a: 1, b: 2, c: 3};

// // console.log(a == b);

// // let arr1 = [1, 2, 3];
// // let arr2 = [4, 5, 6];
// // let arr3 = [...arr1, ...arr2];

// // console.log(arr1+arr2);
// // console.log(arr3);

// // let a = prompt("입력: ");

// // if (a >= 90)
// // {
// //     console.log('A');
// // }
// // else if(a >= 80)
// // {
// //     console.log('B');
// // }
// // else if(a >= 70)
// // {
// //     console.log('C');
// // }
// // else if(a >= 60)
// // {
// //     console.log('D');
// // }
// // else
// // {
// //     console.log('F');
// // }

// // let score = prompt("성적 입력: ");

// let a = 0;
// let b = 0;
// // while ( a < 10){
// //     a += 1;
// //     b += a;
// // }
// // console.log(b);

// do{
//     a += 1;
//     b += a;
// }
// while (a < 10);

// console.log(b);


// let a = 486486486486;

// do {
//     let b = prompt("비밀번호 입력해주세요: ");
//     if ((b / 1000000000) >= 1)
//     {
//         if (a == b)
//         {
//             console.log("정답입니다.");
//             break;
//         }
//         else
//         {
//             console.log("오답입니다.");
//         }
//     }
//     else
//     {
//         console.log("비밀번호가 10글자 미만입니다.")
//     }
// }while (true)

// let a = {
//     b: "1",
//     c: 2,
//     d: "3"
// }

// // for (let key in a){
// //     console.log(key)
// // }

// // let array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// // for (let item of array) {
// //     if (item % 2 == 0)
// //     {
// //         console.log(item*10)
// //     }
// // }

// console.log(a.b)
// console.log(a.c)
// console.log(a.d)

// a['d'] = 100

// console.log(a.d)
// a.c = 1000
// console.log(a.c)
// a.e = 10000
// console.log(a.e)
// a['f'] = 100000
// console.log(a.f)

// delete a.f
// console.log(a.f)
// console.log(a)


// class Car {
//     constructor(model, maker, color, year)
//     {
//         this.model = model;
//         this.maker = maker;
//         this.color = color;
//         this.year = year;
//     }

//     drive() {
//         console.log("driving");
//     }

//     stop() {
//         console.log("stop");
//     }
// }

// let car = new Car("sonata", "hyundai", "white", 2022)
// console.log(car)
// car.drive()
// car.stop()

class Chobo{
    constructor(str, dex, agi, int, level, hp)
    {
        this.str = str;
        this.dex = dex;
        this.agi = agi;
        this.int = int;
        this.level = level;
        this.hp = hp;
    }

    attack()
    {
        console.log('${this.level*10 + this.str}')
    }
}

let chobo1 = new Chobo(10, 10, 10, 10, 10, 10)
let chobo2 = new Chobo(20, 20, 20, 20, 20, 20)
let chobo3 = new Chobo(30, 30, 30, 30, 30, 30)
chobo1.attack()
chobo2.attack()
chobo3.attack()


