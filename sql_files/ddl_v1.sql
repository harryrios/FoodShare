create schema foodshare_db;

use foodshare_db;

create table account(
    id          bigint not null,
    email       varchar(20) not null unique,
    password    varchar(40) not null,
    acc_type    varchar(10) not null,

    primary key(id),
    check(acc_type='manager'
          or acc_type='shopper')
);

create table pantry_shopper(
    pantry_id     bigint not null,
    shopper_id    bigint not null,
    primary key(pantry_id, shopper_id),
    foreign key(pantry_id) references pantry(id),
    foreign key(shopper_id) references account(id)
);

create table pantry(
    id          bigint not null,
    name    varchar(40) not null,
    manager_id  bigint not null,

    primary key(id),
    foreign key(manager_id) references account(id)
);

create table inventory(
    pantry_id   bigint not null,
    item_id     bigint not null,

    primary key(pantry_id, item_id),
    foreign key(item_id) references inventory_item(id)
);

create table inventory_item(
    id          bigint not null,
    item_type   varchar(20) not null,
    quantity    int not null,
    origin_id   bigint not null,
    expiration_date date,
    description     varchar(200),
    image           bytea,

    primary key(id),
    check(quantity>=0),
    foreign key(origin_id) references transaction(id)
);

create table transaction(
    id          bigint not null,
    shopper_id  bigint not null,
    pantry_id   bigint not null,
    item_id     bigint not null,
    request_time    datetime not null,
    request_status  varchar(10) not null,
    request_action  varchar(10) not null,
    quantity        int not null,
    description     varchar(400) not null,

    primary key(id),
    foreign key(shopper_id) references account(id),
    foreign key(pantry_id, item_id) references inventory(pantry_id,item_id),
    check(request_status='pending'
        or request_status='approved'
        or request_status='denied'
    ),
    check(request_action='receive'
        or request_action='donate'
    ),
    check(quantity>0)
);