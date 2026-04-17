do
$$
declare
   v_first_name actor.first_name%type;
   v_last_name actor.last_name%type;
begin
   -- select the first_name and last_name of the actor id 1
   select first_name, last_name
   into v_first_name, v_last_name
   from actor
   where actor_id = 1;

   -- show the full name
   raise notice '% %', v_first_name, v_last_name;
end;
$$;