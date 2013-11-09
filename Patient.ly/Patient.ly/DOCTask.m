//
//  DOCTask.m
//  Patient.ly
//
//  Created by Angie Lal on 11/8/13.
//  Copyright (c) 2013 Angie Lal. All rights reserved.
//

#import "DOCTask.h"
#import "DOCMasterViewController.h"

@implementation DOCTask
-(DOCTask *)initWithId:(NSNumber *)tid name:(NSString *)name description:(NSString *)description
{
    self = [super init];
    if (self) {
        _tid = tid;
        _name = name;
        _description = description;
    }
    return self;
}

@end
