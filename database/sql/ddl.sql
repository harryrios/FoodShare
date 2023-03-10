-- create schema foodshare_db;


create table account(
    id          bigint not null,
    name        varchar(20) not null unique,
    email       varchar(20) not null unique,
    password    varchar(40) not null,
    account_type    varchar(10) not null,

    primary key(id),
    check(account_type='manager'
          or account_type='shopper')
);


create table pantry(
    id          bigint not null,
    name    varchar(40) not null,
    manager_id  bigint not null,
    address  varchar(40) not null,

    primary key(id),
    foreign key(manager_id) references account(id)
);


create table pantry_shopper(
    pantry_id     bigint not null,
    shopper_id    bigint not null,
    notifications boolean not null,
    primary key(pantry_id, shopper_id),
    foreign key(pantry_id) references pantry(id),
    foreign key(shopper_id) references account(id)
);


create table inventory_item(
    id          bigint not null,
    item_type   varchar(20) not null,
    quantity    int not null,
    expiration_date date,
    summary     varchar(200),
    image           bytea,

    primary key(id),
    check(quantity>=0)
);

create table inventory(
    pantry_id   bigint not null,
    item_id     bigint not null,

    primary key(pantry_id, item_id),
    foreign key(item_id) references inventory_item(id)
);



create table transaction_request(
    id          bigint not null,
    shopper_id  bigint not null,
    pantry_id   bigint not null,
    item_id     bigint,
    request_time    timestamp not null,
    request_status  varchar(10) not null,
    request_action  varchar(10) not null,
    quantity        int not null,
    summary     varchar(400) not null,
    anonymous   bool,

    primary key(id),
    foreign key(shopper_id) references account(id),
    foreign key(pantry_id) references pantry(id),
    foreign key(item_id) references inventory_item(id),
    check(request_status='pending'
        or request_status='approved'
        or request_status='denied'
    ),
    check(request_action='receive'
        or request_action='donate'
    ),
    check(quantity>0)
);
