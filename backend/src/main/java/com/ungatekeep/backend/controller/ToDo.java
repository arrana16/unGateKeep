package com.ungatekeep.backend.controller;

import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.Map;


@RestController
public class ToDo {
    ArrayList<String> tasks = new ArrayList<String>();

    @GetMapping("/tasks")
    public ArrayList<String> getTasks() {
        return tasks;
    }

    @PostMapping("/tasks")
    public String addTask(@RequestBody Task task) {
        tasks.add(task.getTask());

        System.out.println(task);
        return task.getTask();
    }

    @DeleteMapping("/tasks")
    public String deleteTask(@RequestBody Task task) {
        boolean isRemoved = false;
        for (int i = 0; i<tasks.size(); i++) {
            if (tasks.get(i).equals(task.getTask())){
                tasks.remove(i);
                isRemoved = true;
            }
        }

        if (isRemoved) {
            return "Task deleted successfully";
        } else {
            return "Task not found";
        }
    }


}


